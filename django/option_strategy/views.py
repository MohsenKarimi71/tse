from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tse_downloader.models import Option, Stock
from option_visualizer.templatetags.date_filters import to_jalali, days_remaining

SELL_BUY_COMMISSION = Decimal('1.26')
OPTION_SELL_BUY_COMMISSION = Decimal('0.21')

def get_covered_call_sterategy_data(stock_price, premium, strike_price, status, remained_days):
    remained_days = remained_days
    cost = (stock_price * (1 + (SELL_BUY_COMMISSION / 100))) - (premium * (1 - (OPTION_SELL_BUY_COMMISSION / 100)))
    if status == "itm":
        current_profit = strike_price - cost
        current_profit_percent = round((current_profit / cost) * 100, 1)
        max_profit_percent = current_profit_percent

        if current_profit > 0:
            no_risk_range = round((((stock_price - cost) / stock_price)) * 100 ,1)
            yearly_profit_percent = round((((1 + (current_profit / cost)) ** Decimal(365 / remained_days)) - 1) * 100, 1)
            risk_score = round(no_risk_range / Decimal(remained_days ** 0.5), 2)
        else:
            no_risk_range = 0
            yearly_profit_percent = 0
            risk_score = 0
    else:
        current_profit = (premium * (1 - (OPTION_SELL_BUY_COMMISSION / 100))) - (stock_price * (SELL_BUY_COMMISSION / 100))
        current_profit_percent = round((current_profit / cost) * 100, 1)
        max_profit = (strike_price - (strike_price - stock_price) * (SELL_BUY_COMMISSION / 100)) - cost
        max_profit_percent = round((max_profit / cost) * 100, 1)

        no_risk_range = round((((stock_price - cost) / stock_price)) * 100 ,1)
        risk_score = round(no_risk_range / Decimal(remained_days ** 0.5), 2)

    if current_profit_percent > 0:
        daily_profit_percent = round(current_profit_percent / remained_days, 2)
        yearly_profit_percent = round((((1 + (current_profit / cost)) ** Decimal(365 / remained_days)) - 1) * 100, 1)
    else:
        daily_profit_percent = 0
        yearly_profit_percent = 0

    return current_profit_percent, max_profit_percent, daily_profit_percent, yearly_profit_percent, no_risk_range, risk_score
    

@csrf_exempt
def get_all_contracts_covered_call_data(request):
    # calculate the covered-call starategy info for call contracts
    all_option_chain = Stock.objects.filter(is_in_option_chain=True)

    if request.method == "GET":
        return render(request, "option_strategy/covered_call_all.html", context={"stocks":all_option_chain})
    
    elif request.method == "POST":
        params = json.loads(request.body)

        selected_stocks = params.get('stocks')
        min_deal_count = params.get('min_deal_count')
        min_deal_volume = params.get('min_deal_volume')
        min_deal_value = params.get('min_deal_value')

        if selected_stocks:
            filtered_option_chain = Stock.objects.filter(pk__in=selected_stocks)
        else:
            filtered_option_chain = all_option_chain

        call_contracts = []
        stock_prices = []

        # get call contracts of stocks in option chain only if price of stock exists
        for stock in filtered_option_chain:
            stock_price = stock.prices.order_by('-timestamp').first()
            if(stock_price):
                if(stock_price.price != 0):
                    stock_price = stock_price.price
                    call_contracts += list(Option.objects.filter(stock=stock.pk, contract_type="BUY").order_by("-expiration_date", "strike_price"))
            
                    for i in range(len(call_contracts) - len(stock_prices)):
                        stock_prices.append(stock_price)
                else:
                    print("Stock price is zero ==> ", stock.symbol)
            else:
                print("No stock price: ", stock.symbol)
        
        all_call_contracts_count = len(call_contracts)

        data = {
            "itm": [],
            "otm": []
        }
        with_no_deal_price = 0
        for i in range(len(call_contracts) - 1, -1, -1):
            contract = call_contracts[i]
            price = contract.prices.order_by('-timestamp').first()
            remained_days = days_remaining(contract.expiration_date)

            if(price):
                if(price.deal_count >= int(min_deal_count)):
                    if(price.deal_volume >= int(min_deal_volume)):
                        if(price.deal_value >= int(min_deal_value)):                            
                            if contract.strike_price <= stock_prices[i]:
                                key = "itm"
                                current_profit, max_profit, daily_profit_percent, yearly_profit_percent, no_risk_range, risk_score = get_covered_call_sterategy_data(
                                    stock_prices[i],
                                    price.buy_bid_price,
                                    contract.strike_price,
                                    key,
                                    remained_days
                                )
                            else:
                                key = "otm"
                                current_profit, max_profit, daily_profit_percent, yearly_profit_percent, no_risk_range, risk_score = get_covered_call_sterategy_data(
                                    stock_prices[i],
                                    price.buy_bid_price,
                                    contract.strike_price,
                                    key,
                                    remained_days
                                )

                            if(current_profit > 0):
                                data[key].append({
                                    'stock':contract.stock.symbol,
                                    'contract_type':contract.get_contract_type_display(),
                                    'strike_price':contract.strike_price,
                                    'expiration_date': to_jalali(contract.expiration_date),
                                    'days_remaining':remained_days,
                                    'deal_count':price.deal_count,
                                    'deal_volume':price.deal_volume,
                                    'deal_value':price.deal_value,
                                    'last_deal_price':price.last_deal_price,
                                    'buy_bid_price':price.buy_bid_price,
                                    'sell_bid_price':price.sell_bid_price,
                                    'stock_price':stock_prices[i],
                                    'current_profit':current_profit,
                                    'max_profit':max_profit,
                                    'daily_profit_percent':daily_profit_percent,
                                    'yearly_profit_percent':yearly_profit_percent,
                                    'no_risk_range':no_risk_range,
                                    'risk_score':risk_score,
                                })
                            else:
                                del call_contracts[i]
                                del stock_prices[i]
                        else:
                            del call_contracts[i]
                            del stock_prices[i]
                    else:
                        del call_contracts[i]
                        del stock_prices[i]
                else:
                    del call_contracts[i]
                    del stock_prices[i]
            else:
                with_no_deal_price += 1
                del call_contracts[i]
                del stock_prices[i]
        data['itm'].sort(key=lambda dic: dic['yearly_profit_percent'], reverse=True)
        data['otm'].sort(key=lambda dic: dic['yearly_profit_percent'], reverse=True)
        return JsonResponse({
            'data':data,
            "all_call_contracts_count":all_call_contracts_count,
            "call_contracts_with_deal_price_count":all_call_contracts_count - with_no_deal_price,
            "filtered_call_contracts_count":len(data['itm']) + len(data['otm']),
            # "stocks":list(all_option_chain.values()),
        })

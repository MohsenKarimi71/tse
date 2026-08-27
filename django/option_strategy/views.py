from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from collections import defaultdict

from tse_downloader.models import Option, Stock
from option_visualizer.templatetags.date_filters import to_jalali, days_remaining

SELL_BUY_COMMISSION = Decimal('1.26')
OPTION_SELL_BUY_COMMISSION = Decimal('0.21')

"""
STRATEGIES HELPER FUNCTIONS
"""

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
    

def get_bull_call_spread_strategy_data(long_strike, short_strike, buy_leg_price, sell_leg_price, remained_days):
    """
    Bull Call Spread:
    - Buy Call at lower strike (K1) at buy_leg_price (sell_bid_price / best ask)
    - Sell Call at higher strike (K2) at sell_leg_price (buy_bid_price / best bid)
    """
    # Cost to buy the lower strike call (including option fee)
    long_cost = buy_leg_price * (1 + (OPTION_SELL_BUY_COMMISSION / Decimal('100')))
    # Revenue received from selling higher strike call (minus option fee)
    short_revenue = sell_leg_price * (1 - (OPTION_SELL_BUY_COMMISSION / Decimal('100')))
    
    # Net Debit (Total initial cost / Max Risk)
    net_debit = long_cost - short_revenue
    if net_debit <= 0:
        return None  # Skip zero or negative debit scenarios

    strike_difference = short_strike - long_strike
    
    # Max Profit = (K2 - K1) - Net Debit
    max_profit = strike_difference - net_debit
    if max_profit <= 0:
        return None

    # Returns & Ratios
    max_profit_percent = round(float(max_profit / net_debit) * 100, 1)
    breakeven_price = long_strike + net_debit
    risk_reward_ratio = round(float(max_profit / net_debit), 2)

    if remained_days > 0 and max_profit_percent > 0:
        daily_profit_percent = round(max_profit_percent / remained_days, 2)
        try:
            # Use standard float arithmetic for compound annualization to prevent Decimal overflow
            profit_ratio = float(max_profit / net_debit)
            yearly_compound = ((1 + profit_ratio) ** (365.0 / float(remained_days)) - 1) * 100.0
            yearly_profit_percent = round(yearly_compound, 1)
        except (OverflowError, ValueError):
            yearly_profit_percent = 9999.0
    else:
        daily_profit_percent = 0
        yearly_profit_percent = 0

    return {
        'net_debit': round(net_debit, 2),
        'max_profit': round(max_profit, 2),
        'max_profit_percent': max_profit_percent,
        'breakeven_price': round(breakeven_price, 2),
        'risk_reward_ratio': risk_reward_ratio,
        'daily_profit_percent': daily_profit_percent,
        'yearly_profit_percent': yearly_profit_percent,
    }

    
"""
STRATEGIES FUNCTIONS
"""

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


@csrf_exempt
def get_all_contracts_bull_call_spread_data(request):
    all_option_chain = Stock.objects.filter(is_in_option_chain=True)

    if request.method == "GET":
        return render(request, "option_strategy/bull_call_spread_all.html", context={"stocks": all_option_chain})

    elif request.method == "POST":
        params = json.loads(request.body)

        selected_stocks = params.get('stocks')
        min_deal_count = int(params.get('min_deal_count', 0))
        min_deal_volume = int(params.get('min_deal_volume', 0))
        min_deal_value = int(params.get('min_deal_value', 0))

        if selected_stocks:
            filtered_option_chain = Stock.objects.filter(pk__in=selected_stocks)
        else:
            filtered_option_chain = all_option_chain

        spread_opportunities = []
        total_pairs_evaluated = 0

        for stock in filtered_option_chain:
            stock_price_obj = stock.prices.order_by('-timestamp').first()
            if not stock_price_obj or stock_price_obj.price == 0:
                continue

            current_stock_price = stock_price_obj.price

            # Fetch all BUY contracts for this stock
            call_contracts = Option.objects.filter(
                stock=stock,
                contract_type="BUY"
            ).order_by("strike_price")

            # Group contracts by expiration_date
            contracts_by_expiry = defaultdict(list)
            for contract in call_contracts:
                price = contract.prices.order_by('-timestamp').first()
                # Liquidity & quote validation
                if (price and 
                    price.deal_count >= min_deal_count and 
                    price.deal_volume >= min_deal_volume and 
                    price.deal_value >= min_deal_value and
                    price.sell_bid_price > 0 and 
                    price.buy_bid_price > 0):
                    contracts_by_expiry[contract.expiration_date].append((contract, price))

            # Pair contracts per expiration date (K1 < K2)
            for expiry_date, contracts in contracts_by_expiry.items():
                remained_days = days_remaining(expiry_date)
                if remained_days <= 0:
                    continue

                contracts_count = len(contracts)
                for i in range(contracts_count):
                    long_contract, long_price = contracts[i]

                    for j in range(i + 1, contracts_count):
                        short_contract, short_price = contracts[j]

                        # Ensure strike price condition K1 < K2
                        if long_contract.strike_price >= short_contract.strike_price:
                            continue

                        total_pairs_evaluated += 1

                        # Buy long leg at best ask (sell_bid_price), sell short leg at best bid (buy_bid_price)
                        calc = get_bull_call_spread_strategy_data(
                            long_strike=long_contract.strike_price,
                            short_strike=short_contract.strike_price,
                            buy_leg_price=long_price.sell_bid_price,
                            sell_leg_price=short_price.buy_bid_price,
                            remained_days=remained_days
                        )

                        if calc and calc['max_profit_percent'] > 0:
                            spread_opportunities.append({
                                'stock': stock.symbol,
                                'stock_price': current_stock_price,
                                'expiration_date': to_jalali(expiry_date),
                                'days_remaining': remained_days,
                                # Long Leg (Buy low strike)
                                'long_strike': long_contract.strike_price,
                                'long_buy_price': long_price.sell_bid_price,
                                'long_deal_volume': long_price.deal_volume,
                                # Short Leg (Sell high strike)
                                'short_strike': short_contract.strike_price,
                                'short_sell_price': short_price.buy_bid_price,
                                'short_deal_volume': short_price.deal_volume,
                                # Strategy Metrics
                                'net_debit': calc['net_debit'],
                                'max_profit': calc['max_profit'],
                                'max_profit_percent': calc['max_profit_percent'],
                                'breakeven_price': calc['breakeven_price'],
                                'risk_reward_ratio': calc['risk_reward_ratio'],
                                'daily_profit_percent': calc['daily_profit_percent'],
                                'yearly_profit_percent': calc['yearly_profit_percent'],
                            })

        spread_opportunities.sort(key=lambda dic: dic['yearly_profit_percent'], reverse=True)

        return JsonResponse({
            'data': spread_opportunities,
            'total_pairs_evaluated': total_pairs_evaluated,
            'filtered_spreads_count': len(spread_opportunities),
        })

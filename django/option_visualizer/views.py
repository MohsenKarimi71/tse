from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tse_downloader.models import Option, Stock
from .templatetags.date_filters import to_jalali, days_remaining


def get_option_chain_list(request):
    option_chain = Stock.objects.filter(is_in_option_chain=True)
    return render(request, "option_visualizer/option_chain.html", context={"option_chain": option_chain})


def get_option_contracts(request, pk):
    # return option contracts of a the given stock based on the query parameters
    min_deal_count = request.GET.get('deal_count', 1)
    min_deal_volume = request.GET.get('deal_volume', 1)
    min_deal_value = request.GET.get('deal_value', 1)

    # get option contracts of the option stock
    option_contracts = list(Option.objects.filter(stock=pk).order_by("-expiration_date", "strike_price", "contract_type"))
    all_contracts_count = len(option_contracts)
    
    # get data of the last price of each contract
    option_prices = []

    for i in range(len(option_contracts) - 1, -1, -1):
        price = option_contracts[i].prices.order_by('-timestamp').first()
        if(price):
            if(price.deal_count >= int(min_deal_count)):
                if(price.deal_volume >= int(min_deal_volume)):
                    if(price.deal_value >= int(min_deal_value)):
                        option_prices.append(price)
                    else:
                        del option_contracts[i]
                else:
                    del option_contracts[i]
            else:
                del option_contracts[i]
        else:
            del option_contracts[i]
    for contract in option_contracts:
        option_prices.append(contract.prices.order_by('-timestamp').first())

    return render(request, "option_visualizer/option_contracts.html", context={
        "option_contracts_prices": zip(option_contracts, option_prices),
        "option": Stock.objects.get(pk=pk),
        "all_contracts_count":all_contracts_count,
        "contracts_count":len(option_contracts),
    })

@csrf_exempt
def get_all_options_contracts(request):
    # return all option contracts based on the query parameters
    all_option_chain = Stock.objects.filter(is_in_option_chain=True)

    if request.method == "GET":
        option_contracts = []
        stock_prices = []

        # get contracts of all stocks in option chain
        for stock in all_option_chain:
            stock_price = stock.prices.order_by('-timestamp').first()
            if stock_price:
                stock_price = stock_price.price
            else:
                stock_price = 0

            option_contracts += list(Option.objects.filter(stock=stock.pk).order_by("-expiration_date", "strike_price", "contract_type"))
            for i in range(len(option_contracts) - len(stock_prices)):
                stock_prices.append(stock_price)

        all_contracts_count = len(option_contracts)
        # get data of the last price of each contract
        option_prices = []
        for contract in option_contracts:
            option_prices.append(contract.prices.order_by('-timestamp').first())
        
        return render(request, "option_visualizer/all_options_contracts.html", context={"stocks":all_option_chain})
    
    elif request.method == "POST":
        params = json.loads(request.body)

        selected_stocks = params.get('stocks')
        contract_type = params.get('contract_type')

        if selected_stocks:
            filtered_option_chain = Stock.objects.filter(pk__in=selected_stocks)
        else:
            filtered_option_chain = all_option_chain
        option_contracts = []
        stock_prices = []

        # get contracts of all stocks in option chain
        for stock in filtered_option_chain:
            stock_price = stock.prices.order_by('-timestamp').first()
            if stock_price:
                stock_price = stock_price.price
            else:
                stock_price = 0

            if(contract_type == "all"):
                option_contracts += list(Option.objects.filter(stock=stock.pk).order_by("-expiration_date", "strike_price", "contract_type"))
            else:
                option_contracts += list(Option.objects.filter(stock=stock.pk, contract_type=contract_type).order_by("-expiration_date", "strike_price"))
            for i in range(len(option_contracts) - len(stock_prices)):
                stock_prices.append(stock_price)

        data = []
        for contract in option_contracts:
            dic = {
                'stock':contract.stock.symbol,
                'contract_type':contract.get_contract_type_display(),
                'strike_price':contract.strike_price,
                'expiration_date': to_jalali(contract.expiration_date),
                'days_remaining':days_remaining(contract.expiration_date),
            }

            data.append(dic)

            # price = contract.prices.order_by('-timestamp').first()

            # if(price):
            #     if(price.deal_count >= int(min_deal_count)):
            #         if(price.deal_volume >= int(min_deal_volume)):
            #             if(price.deal_value >= int(min_deal_value)):
            #                 dic['deal_count'] = price.deal_count
            #                 dic['deal_volume'] = price.deal_volume
            #                 dic['deal_value'] = price.deal_value
            #                 dic['last_deal_price'] = price.last_deal_price
            #                 dic['buy_bid_price'] = price.buy_bid_price
            #                 dic['sell_bid_price'] = price.sell_bid_price
            #                 dic['stock_price'] = stock_prices[i]

            #                 data.append(dic)
            #             else:
            #                 del option_contracts[i]
            #                 del stock_prices[i]
            #         else:
            #             del option_contracts[i]
            #             del stock_prices[i]
            #     else:
            #         del option_contracts[i]
            #         del stock_prices[i]
            # else:
            #     del option_contracts[i]
            #     del stock_prices[i]
        
        return JsonResponse({
            'data':data,
            "all_contracts_count":len(Option.objects.all()),
            "contracts_count":len(data),
            "stocks":list(all_option_chain.values()),
        })

    

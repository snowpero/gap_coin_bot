#-*- coding: utf-8 -*-

import urllib
import urllib2
import json
import global_value as gv

bithumb_api = 'https://api.bithumb.com/public/ticker/'
upbit_api = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-'
upbit_json_api = 'https://static.upbit.com/crypto-currency-deposit-desc/{coin_name}.json'
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'}

class CoinTicker():
    # def get(self):
    #     bithumb_price = self.get_bithumb_price()
    #     upbit_price = self.get_upbit_price()

    #     print('bithumb : ' + str(bithumb_price) + ', upbit : ' + str(upbit_price))

    #     f_bithumb_price = float(bithumb_price)
    #     f_upbit_price = float(upbit_price)
    #     f_gap = f_bithumb_price - f_upbit_price

    #     if f_gap < 0:
    #         f_gap = -1 * f_gap
    #     print('gap : ' + str(f_gap))

    #     percent_gap_bithumb = f_gap / f_bithumb_price * 100
    #     percent_gap_upbit = f_gap / f_upbit_price * 100

    #     print('percent gap bithumb : ' + str(percent_gap_bithumb) + ', upbit : ' + str(percent_gap_upbit))

    #     return {
    #         "bithumb_price" : bithumb_price,
    #         "bithumb_gap" : percent_gap_bithumb,
    #         "upbit_price" : upbit_price,
    #         "upbit_gap" : percent_gap_upbit,
    #         "gap_krw" : f_gap
    #     }

    def get_data(self, coin_name):
        bithumb_price = self.get_bithumb_price(coin_name)
        upbit_price = self.get_upbit_price(coin_name)

        print('Coin : ' + coin_name)
        print('bithumb : ' + str(bithumb_price) + ', upbit : ' + str(upbit_price))

        f_bithumb_price = float(bithumb_price)
        f_upbit_price = float(upbit_price)
        f_gap = f_bithumb_price - f_upbit_price

        if f_gap < 0:
            f_gap = -1 * f_gap
        print('gap : ' + str(f_gap))

        percent_gap_bithumb = f_gap / f_bithumb_price * 100
        percent_gap_upbit = f_gap / f_upbit_price * 100

        print('percent gap bithumb : ' + str(percent_gap_bithumb) + ', upbit : ' + str(percent_gap_upbit))

        return {
            "bithumb_price" : bithumb_price,
            "bithumb_gap" : percent_gap_bithumb,
            "upbit_price" : upbit_price,
            "upbit_gap" : percent_gap_upbit,
            "gap_krw" : f_gap,
            "coin_name" : coin_name
        }

    def get_bithumb_price(self, coin_name):
        body_bithumb = urllib2.urlopen(bithumb_api + coin_name).read()
        json_bithumb = json.loads(body_bithumb)

        retValue = json_bithumb['data']['buy_price']
        return str(retValue)

    def check_bithumb_ticker_listed(self, coin_name):
        try:
            urllib2.urlopen(bithumb_api + coin_name)
        except urllib2.HTTPError, e:
            return False
        except Exception:
            return False

        return True
    
    def check_upbit_desc_listed(self, coin_name):
        try:
            req_api = upbit_json_api.replace('{coin_name}', coin_name)
            req_upbit = urllib2.Request(req_api, headers=hdr)
            json_upbit = json.load(urllib2.urlopen(req_upbit))       
        except urllib2.HTTPError, e:
            return False
        except Exception:
            return False

        return True

    def get_upbit_price(self, coin_name):
        req_upbit = urllib2.Request(upbit_api + coin_name, headers=hdr)
        json_upbit = json.load(urllib2.urlopen(req_upbit))

        retValue = json_upbit[0]['tradePrice']
        return str(retValue)
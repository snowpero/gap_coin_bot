#-*- coding: utf-8 -*-

import urllib
import urllib2
import json
import global_value as gv

bithumb_api = 'https://api.bithumb.com/public/ticker/DASH'
upbit_api = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-DASH'
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'}

class DASHTicker:
    def get(self):
        bithumb_price = self.get_bithumb_price()
        upbit_price = self.get_upbit_price()

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

        gv.bithumb_eos = bithumb_price
        gv.bithumb_eos_gap = percent_gap_bithumb
        gv.upbit_eos = upbit_price
        gv.upbit_eos_gap = percent_gap_upbit
        gv.eos_gap_krw = f_gap        

    def get_bithumb_price(self):
        body_bithumb = urllib2.urlopen(bithumb_api).read()
        json_bithumb = json.loads(body_bithumb)

        retValue = json_bithumb['data']['buy_price']
        return str(retValue)

    def get_upbit_price(self):
        req_upbit = urllib2.Request(upbit_api, headers=hdr)
        json_upbit = json.load(urllib2.urlopen(req_upbit))

        retValue = json_upbit[0]['tradePrice']
        return str(retValue)
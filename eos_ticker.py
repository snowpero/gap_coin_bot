#-*- coding: utf-8 -*-

import urllib
import urllib2
import json
import global_value as gv

# bitthumb https://api.bithumb.com/public/ticker/EOS
# upbit https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-EOS

bithumb_api = 'https://api.bithumb.com/public/ticker/EOS'
upbit_api = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-EOS'
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'}

class EOSTicker:
    def get(self):
        bithumb_eos = self.get_bithumb_eos()
        upbit_eos = self.get_upbit_eos()

        print('bithumb : ' + str(bithumb_eos) + ', upbit : ' + str(upbit_eos))

        f_bithumb_eos = float(bithumb_eos)
        f_upbit_eos = float(upbit_eos)
        f_gap = f_bithumb_eos - f_upbit_eos

        if f_gap < 0:
            f_gap = -1 * f_gap
        print('gap : ' + str(f_gap))

        percent_gap_bithumb = f_gap / f_bithumb_eos * 100
        percent_gap_upbit = f_gap / f_upbit_eos * 100

        print('percent gap bithumb : ' + str(percent_gap_bithumb) + ', upbit : ' + str(percent_gap_upbit))

        gv.bithumb_eos = bithumb_eos
        gv.bithumb_gap = percent_gap_bithumb
        gv.upbit_eos = upbit_eos
        gv.upbit_gap = percent_gap_upbit
        gv.gap_krw = f_gap        

    def get_bithumb_eos(self):
        body_bithumb = urllib2.urlopen(bithumb_api).read() #urlfetch.fetch(bithumb_api)
        json_bithumb = json.loads(body_bithumb)
        # print('bithumb req\n' + str(json_bithumb))

        # json_data = json.load(req_bithumb)
        retValue = json_bithumb['data']['buy_price']
        # print('bithumb_eos : ' + str(retValue))
        return str(retValue)

    def get_upbit_eos(self):
        req_upbit = urllib2.Request(upbit_api, headers=hdr)
        json_upbit = json.load(urllib2.urlopen(req_upbit))
        # print('upbit req\n' + str(json_upbit))

        # json_data = json.load(req_upbit)
        retValue = json_upbit[0]['tradePrice']
        # print('upbit_eos : ' + str(retValue))
        return str(retValue)
        # print('Test')
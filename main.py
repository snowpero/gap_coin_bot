#-*- coding: utf-8 -*-

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import datetime
import logging
import eos_ticker
import coin_ticker
from coin_price_data import CoinPriceData
import global_value as gv
import pytz
from pytz import timezone
from telegram_bot import broadcast

gap_threshold = 2

class MainPage(webapp2.RequestHandler):
    def get(self):
        # eos_instance = eos_ticker.EOSTicker()
        # eos_instance.get()

        # # HTML 페이지 노출용
        # message = 'EOS Price!!<p>'
        # message += '빗썸 EOS : %s<p>업비트 EOS : %s<p>가격차이 : %s 원<p>' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.eos_gap_krw))
        # message += '빗썸 가격차이 비율 : %.4f%%<p>업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_eos_gap, gv.upbit_eos_gap)

        # self.response.write(message)

        # # 텔레그램 메세지용
        # telegram_msg = u'EOS Price!!\n'
        # telegram_msg += u'빗썸 EOS : %s\n업비트 EOS : %s\n가격차이 : %s원\n' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.eos_gap_krw))
        # telegram_msg += u'빗썸 가격차이 비율 : %.4f%%\n업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_eos_gap, gv.upbit_eos_gap)
        # broadcast(telegram_msg)

        coin_ticker_instance = coin_ticker.CoinTicker()
        coin_data = coin_ticker_instance.get_data('DASH')

        # HTML 페이지 노출용
        message = '%s Price!! (기준 시간 : %s) <p>' % (str(coin_data['coin_name']), str(self.check_time()))
        message += '빗썸 : %s 원<p>업비트 : %s 원<p>가격차이 : %s 원<p>' % (str(coin_data['bithumb_price']), str(coin_data['upbit_price']), str(coin_data['gap_krw']))
        message += '빗썸 가격차이 비율 : %.4f%%<p>업비트 가격차이 비율 : %.4f%%' % (coin_data['bithumb_gap'], coin_data['upbit_gap'])

        self.response.write(message)

    def check_time(self):
        nowDate = datetime.datetime.now()

        seoul = timezone('Asia/Seoul')
        loc_dt = seoul.localize(nowDate)
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'

        retTime = loc_dt.strftime(fmt)

        print('Time : ' + retTime)

        return retTime

class CheckOnTime(webapp2.RequestHandler):  

    update_time = ''

    def get(self):        
        update_time = self.check_time()
        print(update_time)

        # eos_instance = eos_ticker.EOSTicker()
        # eos_instance.get()

        # # 메세지 발송 조건 : 1%가 200원 이상 일때 체크
        # check_gap = gv.upbit_eos * 0.01
        # is_under_200_won = True
        # if check_gap > 200:
        #     is_under_200_won = False

        # telegram_msg = u'EOS Price!!\n'
        # telegram_msg += u'빗썸 EOS : %s\n업비트 EOS : %s\n가격차이 : %s원\n' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.eos_gap_krw))
        # telegram_msg += u'빗썸 가격차이 비율 : %.4f%%\n업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_eos_gap, gv.upbit_eos_gap)

        # if is_under_200_won is True :
        #     if gv.bithumb_eos_gap >= gap_threshold or gv.upbit_eos_gap >= gap_threshold :                
        #         broadcast(telegram_msg)
        # else :
        #     broadcast(telegram_msg)

        coin_ticker_instance = coin_ticker.CoinTicker()
        
        eos_data = coin_ticker_instance.get_data('EOS')
        self.check_coin_data(CoinPriceData(eos_data))

        dash_data = coin_ticker_instance.get_data('DASH')
        self.check_coin_data(CoinPriceData(dash_data))

    def check_coin_data(self, coin_data):
        check_send_push_status = self.isEnablePrice(coin_data)

        if check_send_push_status :
            self.sendTelegramMsg(coin_data)

    def check_time(self):
        nowDate = datetime.datetime.now()

        seoul = timezone('Asia/Seoul')
        loc_dt = seoul.localize(nowDate)
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'

        retTime = loc_dt.strftime(fmt)

        return retTime

    def isEnablePrice(self, price_data):
        # 메세지 발송 : gap 이 해당 코인의 1% 이하일 경우
        check_gap = float(price_data.upbit_price) * 0.01        

        # if check_gap > self.price_gap_krw :
        #     if self.bithumb_price_gap >= gap_threshold or self.upbit_price_gap >= gap_threshold :
        #         return True
        #     else :
        #         return False
        # else :
        #     return True

        if price_data.bithumb_price_gap >= gap_threshold or price_data.upbit_price_gap >= gap_threshold :
            return True
        else :
            return False

        # return True

    def sendTelegramMsg(self, price_data):
        telegram_msg = u'%s 가격!! (기준 시간 : %s)\n' % (str(price_data.coin_name), self.check_time())
        telegram_msg += u'빗썸 : %s 원\n업비트 : %s 원\n가격차이 : %s원\n' % (str(price_data.bithumb_price), str(price_data.upbit_price), str(price_data.price_gap_krw))
        telegram_msg += u'빗썸 가격차이 비율 : %.4f%%\n업비트 가격차이 비율 : %.4f%%' % (price_data.bithumb_price_gap, price_data.upbit_price_gap)

        broadcast(telegram_msg)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/task/ontime', CheckOnTime)
], debug=True)

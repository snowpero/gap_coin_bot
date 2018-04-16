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
import global_value as gv
import pytz
from pytz import timezone
from telegram_bot import broadcast

gap_threshold = 2

class MainPage(webapp2.RequestHandler):
    def get(self):
        eos_instance = eos_ticker.EOSTicker()
        eos_instance.get()

        message = 'EOS Price!!<p>'
        message += '빗썸 EOS : %s<p>업비트 EOS : %s<p>가격차이 : %s 원<p>' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.gap_krw))
        message += '빗썸 가격차이 비율 : %.4f%%<p>업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_gap, gv.upbit_gap)

        self.response.write(message)

        telegram_msg = u'EOS Price!!\n'
        telegram_msg += u'빗썸 EOS : %s\n업비트 EOS : %s\n가격차이 : %s원\n' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.gap_krw))
        telegram_msg += u'빗썸 가격차이 비율 : %.4f%%\n업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_gap, gv.upbit_gap)
        broadcast(telegram_msg)

class CheckOnTime(webapp2.RequestHandler):
    def get(self):
        nowDate = datetime.datetime.now()

        seoul = timezone('Asia/Seoul')
        loc_dt = seoul.localize(nowDate)
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        
        gv.prevOnTime = loc_dt.strftime(fmt)
        print(gv.prevOnTime)

        eos_instance = eos_ticker.EOSTicker()
        eos_instance.get()

        # 메세지 발송 조건 : 1%가 200원 이상 일때 체크
        check_gap = gv.upbit_eos * 0.01
        is_under_200_won = True
        if check_gap > 200:
            is_under_200_won = False

        telegram_msg = u'EOS Price!!\n'
        telegram_msg += u'빗썸 EOS : %s\n업비트 EOS : %s\n가격차이 : %s원\n' % (str(gv.bithumb_eos), str(gv.upbit_eos), str(gv.gap_krw))
        telegram_msg += u'빗썸 가격차이 비율 : %.4f%%\n업비트 가격차이 비율 : %.4f%%' % (gv.bithumb_gap, gv.upbit_gap)

        if is_under_200_won is True :
            if gv.bithumb_gap >= gap_threshold or gv.upbit_gap >= gap_threshold :                
                broadcast(telegram_msg)
        else :
            broadcast(telegram_msg)
            

class SendTelegram(webapp2.RequestHandler):
    def get(self):
        print('SendTelegram')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/task/ontime', CheckOnTime)
], debug=True)

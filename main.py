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
from coin_db import CoinDB
from coin_price_data import CoinPriceData
import global_value as gv
import pytz
from pytz import timezone
from telegram_bot import broadcast

gap_threshold = 2

class MainPage(webapp2.RequestHandler):
    def get(self):
        coin_ticker_instance = coin_ticker.CoinTicker()
        coin_data = coin_ticker_instance.get_data('DASH')

        # HTML 페이지 노출용
        message = '%s Price!! (기준 시간 : %s) <p>' % (str(coin_data['coin_name']), str(self.check_time()))
        message += '빗썸 : %s 원<p>업비트 : %s 원<p>가격차이 : %s 원<p>' % (str(coin_data['bithumb_price']), str(coin_data['upbit_price']), str(coin_data['gap_krw']))
        message += '빗썸 가격차이 비율 : %.4f%%<p>업비트 가격차이 비율 : %.4f%%' % (coin_data['bithumb_gap'], coin_data['upbit_gap'])

        self.response.write(message)

        coin_listed_instance = CheckCoinListed()
        coin_listed_instance.check_coin_listed()

        # ret_val1 = coin_ticker_instance.check_upbit_desc_listed('GTO')
        # ret_val2 = coin_ticker_instance.check_upbit_desc_listed('KNC')
        # print('Test : ' + str(ret_val1) + ', ' + str(ret_val2))

    def check_time(self):
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        KST = datetime.datetime.now(timezone('Asia/Seoul'))
        retTime = KST.strftime(fmt)

        print('Time : ' + retTime)

        return retTime

class CheckCoinGap(webapp2.RequestHandler):  

    arr_coins = ['EOS', 'DASH', 'XMR', 'LTC', 'ETH', 'QTUM', 'ETC']

    def get(self):
        coin_ticker_instance = coin_ticker.CoinTicker()

        for coin_name in self.arr_coins:
            eos_data = coin_ticker_instance.get_data(coin_name)
            self.check_coin_data(CoinPriceData(eos_data))

    def check_coin_data(self, coin_data):
        check_send_push_status = self.isEnablePrice(coin_data)

        if check_send_push_status :
            self.sendTelegramMsg(coin_data)

    def check_time(self):
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        KST = datetime.datetime.now(timezone('Asia/Seoul'))
        retTime = KST.strftime(fmt)

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


class CheckCoinListed(webapp2.RequestHandler):
    
    arr_coins = ['KNC', 'HSR', 'NEO', 'EOS', 'XEM', 'OMG', 'MCO', 'GTO', 'XVG', 'ONT']

    arr_coins_bithumb = ['HSR', 'NEO', 'XVG', 'GTO', 'ONT', 'ADA', 'LSK', 'IOST', 'ZIL', 'NANO']
    # HASHED portfolio added
    arr_coins_upbit = ['KNC', 'HSR', 'ONT', 'ELF', 'NPXS', 'WAX', 'REQ', 'RPX', 'CDT', 'LOKI', 
                        'NAS', 'TOMO', 'RMT', 'ITC', 'BFT', 'BLZ', 'QSP', 'BOT', 'ENG', 'AST', 'AMB',
                        'MANA', 'RLC', 'AE'
                        ]

    market_bithumb = 'bithumb'
    market_upbit = 'upbit'

    def get(self):
        self.check_coin_listed()
        return

    def check_coin_listed(self):
        for coin_name in self.arr_coins_bithumb:
            coin_ticker_instance = coin_ticker.CoinTicker()
            is_bithumb_listed = coin_ticker_instance.check_bithumb_ticker_listed(coin_name)
            print('Coin : %s, listed bithumb : %s' % ( coin_name, str(is_bithumb_listed) ))

            query_bithumb_coins = CoinDB.query_coin(coin_name, self.market_bithumb)
            if query_bithumb_coins is None or query_bithumb_coins.count() == 0:
                if is_bithumb_listed is True:
                    print('[Bithumb] Check DB and Add DB')
                    coin = CoinDB(name = coin_name, market = self.market_bithumb)
                    coin.put()
                    self.sendMsgForBithumb(coin_name)

        for coin_name in self.arr_coins_upbit:
            coin_ticker_instance = coin_ticker.CoinTicker()
            is_upbit_listed = coin_ticker_instance.check_upbit_desc_listed(coin_name)
            print('Coin : %s, listed upbit : %s' % ( coin_name, str(is_upbit_listed) ))

            query_upbit_coins = CoinDB.query_coin(coin_name, self.market_upbit)
            if query_upbit_coins is None or query_upbit_coins.count() == 0:
                if is_upbit_listed is True:
                    print('[Upbit] Check DB and Add DB')
                    coin = CoinDB(name = coin_name, market = self.market_upbit)
                    coin.put()
                    self.sendMsgForUpbit(coin_name)

        return

    def sendTelegramMsg(self, coin_name, market):
        telegram_msg = u'%s 코인 %s 거래소 상장!!' % ( str(coin_name), str(market) )
        broadcast(telegram_msg)

    def sendMsgForBithumb(self, coin_name):
        telegram_msg = u'%s 코인 %s 거래소 상장!!' % ( str(coin_name), str(self.market_bithumb) )
        broadcast(telegram_msg)

    def sendMsgForUpbit(self, coin_name):
        telegram_msg = u'%s 코인 %s 거래소 지갑생성!!' % ( str(coin_name), str(self.market_upbit) )
        broadcast(telegram_msg)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/task/ontime', CheckCoinGap),
    ('/task/coinlisted', CheckCoinListed)
], debug=True)

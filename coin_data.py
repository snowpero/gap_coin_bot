#-*- coding: utf-8 -*-

class CoinData:
    
    bithumb_price = 0
    bithumb_price_gap = 0
    upbit_price = 0
    upbit_price_gap = 0
    price_gap_krw = 0
    coin_name = ''
    
    def __init__(self, coin_data) :
        self.bithumb_price = coin_data['bithumb_price']
        self.bithumb_price_gap = coin_data['bithumb_gap']
        self.upbit_price = coin_data['upbit_price']
        self.upbit_price_gap = coin_data['upbit_gap']
        self.price_gap_krw = coin_data['gap_krw']
        self.coin_name = coin_data['coin_name']
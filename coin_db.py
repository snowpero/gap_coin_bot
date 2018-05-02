#-*- coding: utf-8 -*-

from google.appengine.ext import ndb

#Model
class CoinDB(ndb.Model):
    name = ndb.StringProperty()
    notice = ndb.BooleanProperty(default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    market = ndb.StringProperty()

    @classmethod
    def query_coin(self, _name):
        return CoinDB.query(CoinDB.name == str(_name)).order(-CoinDB.date)

    @classmethod
    def query_coin(self, _name, _market):
        return CoinDB.query( 
            ndb.AND(
                CoinDB.name == str(_name),
                CoinDB.market == str(_market)
                )
         ).order(-CoinDB.date)
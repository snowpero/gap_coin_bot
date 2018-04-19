#-*- coding: utf-8 -*-

from google.appengine.ext import ndb

#Model
class CoinDB(ndb.Model):
    name = ndb.StringProperty()
    notice = ndb.BooleanProperty(default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_coin(self, name):
        return CoinDB.query(CoinDB.name == str(name)).order(-CoinDB.date)
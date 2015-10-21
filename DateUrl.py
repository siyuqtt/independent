__author__ = 'siyuqiu'

class DateUrl:

    def __init__(self, date, account):
        self.date = date
        self.urlnum = 0
        self.totaltweet = 0
        self.url_num_dict = {}
        self.account = account

    def getAccountName(self):
        return self.account

    def setTotaltweet(self, num):
        self.totaltweet = num

    def setUrlNum(self, num):
        self.urlnum = num

    def setUrlNumDict(self, url_num_dict):
        self.url_num_dict = url_num_dict

    def urlPerDay(self):
        return self.urlnum

    def AvgTweetsPerUrl(self):
        if self.urlnum == 0:
            return 0
        return self.totaltweet*1.0/self.urlnum

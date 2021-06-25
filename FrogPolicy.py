from xalpha.policy import *
from xalpha import cons
import xalpha as xa
import collections
import datetime
import queue

#
# class Calculate:
#     def xirr(self, actions:collections.OrderedDict, totMoney):
#         l = -9999
#         r = 9999
#         self.__actions = actions
#         for i in range(100):
#             mid = (l + r) / 2.0
#             if self.__bigCheck(mid, totMoney):
#                 r = mid
#             else:
#                 l = mid
#
#         return l
#
#     def __bigCheck(self, targetRate, totMoney):
#         for d in self.__actions:


class FrogPolicy(policy):
    def __init__(self, infoobj, totmoney, times, splitNumber):
        self.startDate = times[0]
        self.endDate = times[-1]
        self.times = times
        self.actions = collections.OrderedDict()
        self.remainCapital = queue.Queue()
        self.splitNumber = splitNumber #分批投入的次数
        super().__init__(infoobj, self.startDate, self.endDate, totmoney)

    def status_gen(self, date:datetime):

        if date in self.aim.specialdate:
            if self.price[self.price["date"] == date].iloc[0].comment > 0:
                return 0.05
            return 0

        elif date in self.times:
            addMoney = 0 if self.remainCapital.empty() else self.remainCapital.get()
            self.actions[date] = self.totmoney + addMoney #这个月定投的1000

            curStatus = pd.DataFrame(data={'date': list(self.actions.keys()), self.aim.code: list(self.actions.values())})
            curTrade = xa.trade(self.aim, curStatus)

            dailyReport = curTrade.dailyreport(date)
            if dailyReport['基金总申购'].values[0] == 0: #没有申购，直接返回定投
                return self.totmoney + addMoney

            report = dailyReport[['基金收益总额', '基金总申购', '投资收益率', '持有份额', '基金现值']]

            if len(self.actions) > 1:   #不知道为什么一个月的时候不能算
                try:
                    irr = curTrade.xirrrate(date)
                except RuntimeError:
                    print('IRR异常啦，当前投资收益率{}'.format(report['投资收益率'].values[0]))
                    return self.totmoney + addMoney

                if report['基金收益总额'].values[0] > 5000 and irr > 0.15 and report['投资收益率'].values[0] >= 0.3:  #要卖了
                    #分成16份重新投资
                    for i in range(self.splitNumber):
                        self.remainCapital.put(int(report['基金现值'].values[0] / self.splitNumber))
                    share = int(report['持有份额'].values[0])

                    self.actions = collections.OrderedDict()
                    return -1*share
            return self.totmoney + addMoney

        else:
            return 0

io = {'save': True, 'fetch': True, 'form': 'csv', 'path': r'D:\Documents\fund_info\\'}
f = xa.fundinfo('163406', **io)
a = FrogPolicy(f, 2000, pd.date_range('2010-04-22', '2020-08-30', freq='WOM-1THU'), 16)
res = xa.trade(f, a.status)
res.dailyreport().to_excel('test.xls')
print(res.xirrrate())

tot = 0
while not a.remainCapital.empty():
    tot += a.remainCapital.get()
print(tot)
# totalRes.v_tradecost()

# print(pd.date_range('2016-01-01', '2020-10-01', freq='WOM-1THU'))


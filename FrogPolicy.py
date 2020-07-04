from xalpha.policy import *
import xalpha as xa
import collections
import datetime
import queue

class FrogPolicy(policy):
    def __init__(self, infoobj, totmoney, times):
        self.startDate = times[0]
        self.endDate = times[-1]
        self.times = times
        self.actions = collections.OrderedDict()
        self.remainCapital = queue.Queue()
        super().__init__(infoobj, self.startDate, self.endDate, totmoney)

    def status_gen(self, date:datetime):
        print(date.strftime('%Y-%m-%d'))
        print(self.end)

        if date in self.aim.specialdate:
            if self.price[self.price["date"] == date].iloc[0].comment > 0:
                return 0.05
            return 0

        elif date in self.times:
            # print(date)
            self.actions[date] = 1000
            curStatus = pd.DataFrame(data={'date': list(self.actions.keys()), self.aim.code: list(self.actions.values())})
            curTrade = xa.trade(self.aim, curStatus)
            report = curTrade.dailyreport(date)[['基金收益总额', '基金总申购', '投资收益率', '持有份额', '基金现值']]

            if len(self.actions) > 1:   #不知道为什么一个月的时候不能算
                irr = curTrade.xirrrate(date)
                if report['基金收益总额'].values[0] > 5000 and irr > 0.15 and report['投资收益率'].values[0] >= 0.3:  #要卖了
                    #分成16份重新投资
                    for i in range(16):
                        self.remainCapital.put(report['基金现值'].values[0] / 16)
                    share = myround(report['持有份额'].values[0])
                    return -1*share
            return 1000 + 0 if self.remainCapital.empty() else self.remainCapital.get() + sum(self.remainCapital) if date == self.endDate else 0

        else:
            return 0

f = xa.FundInfo('163406')
a = FrogPolicy(f, 1000, pd.date_range('2016-04-01', '2020-07-01', freq='WOM-1THU'))
res = xa.trade(f, a.status)
res.dailyreport().to_excel('test.xls')
# res.v_tradecost()

# print(pd.date_range('2016-01-01', '2020-10-01', freq='WOM-1THU'))


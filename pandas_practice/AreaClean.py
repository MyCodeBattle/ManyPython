import pandas as pd
from dingtalkchatbot.chatbot import *
import arrow

class AreaClean:
    def run(self):
        with open('areaList', 'r', encoding='utf-8') as fp:
            areas = fp.read().split()
        df = pd.read_excel('全国区划代码.xlsx', dtype=str).fillna('').replace(r'\s', '', regex=True)


        output = set()
        for area in areas:
            for idx, row in df.iterrows():
                if row['区县'] in area and (row['设区市'] in area or row['设区市'].replace('市', '') in area):
                    output.add(f'{row["设区市"] + row["区县"]}')

        t = arrow.now()

        bot = DingtalkChatbot('https://oapi.dingtalk.com/robot/send?access_token=39ef33b930e81f4bb15cbf52a1833ef069af54722c7067853e799b3078885d1c')

        words = ''
        words = f'#友情提示#：截至{t.month}月{t.day}日，全国中高风险地区如下↓↓\n'
        words += '\n'.join(sorted(list(output)))
        bot.send_text(words)

if __name__ == '__main__':
    a = AreaClean()
    a.run()

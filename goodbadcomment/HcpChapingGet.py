import pandas as pd
from loguru import logger
import arrow
import time
import json
import requests
import tqdm
from retrying import retry

headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': 'G_zj_gsid=08890c40500a4a8ab21e0b2b9e9e47b1-gsid-', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

index = 1
df = pd.DataFrame()
while True:
    reqBody = {"pageNum": index, "pageSize": 20, "createTimeFrom": 1609430400000, "createTimeTo": 1623227340000, "channelList": [], "areaList": ["ff8080815d551320015d589cc1da0014", "ff8080815d551320015d589cc1da0014$0", "ff8080815df350d4015df3d64603057a", "ff8080815df350d4015df4333f0006cb", "ff8080815df350d4015df44090fd06f5", "ff8080815df350d4015df44e7d100706", "ff8080815de36663015de3e0d0380000", "ff8080815de36663015de3ef492c0015", "ff8080815df45323015df461a0e6000b", "ff8080815df482ba015df7dceec40326", "ff8080815df45323015df46e7610001d", "ff8080815df482ba015df7eb3a8c0367", "ff8080815df45323015df47feebf0116", "ff8080815dfd3779015dfdc8850c06c5", "ff8080815dfc9cb1015dfcf0c19f109f", "bb4a9da3634a58f601636c22dc381288d", "bb4a9da3634a58f601636c22583f125b", "ff8080816f12372d016f1d5959bb7545"], "statusList": []}
    res = json.loads(requests.post(url = 'https://opt.zjzwfw.gov.cn/rest/api/evaluation/case/historyForHandle/list?ctoken=4300b7fc-1f14-4591-a460-b58da21841d3', json=reqBody, headers = headers).text)
    # print(res)
    if not res['data']['list']:
        break

    df = df.append(pd.DataFrame(res['data']['list']), ignore_index=True)
    index += 1
    time.sleep(0.5)

df.to_excel('好差评结果.xls', index=False)


df = pd.read_excel('好差评结果.xls', dtype=str)
resDf = pd.DataFrame()

process = tqdm.tqdm(total=df.shape[0], ncols=200)

for idx, row in df.iterrows():
    res = json.loads(requests.get(url='https://opt.zjzwfw.gov.cn/rest/api/evaluation/detail?ctoken=598cd51b-5ecf-49f6-8e1d-e503d20df4de&id={}&isQueryCaseInfo=true&portalTyp=G'.format(row['evaluationId']), headers=headers).text)['data']

    #申诉理由
    appealReason = res['caseDTO']['appealReason']

    #驳回理由
    failedReason = res['caseDTO']['failedReason']

    #差评人联系方式
    phone = res['raterInfoDTO']['phoneNum']

    #整改理由
    solution = res['caseDTO']['solution']

    #追评等级
    plusCommentDTO = res['feedbackItemDTOList']

    row['申诉理由'] = appealReason
    row['驳回理由'] = failedReason
    row['整改回复'] = solution
    row['差评人手机'] = phone

    if plusCommentDTO:
        plusCommentDTO = plusCommentDTO[0]
        row['追评等级'] = plusCommentDTO['levelDesc']
        row['追评文本'] = plusCommentDTO['rateText']

    resDf = resDf.append(row)
    time.sleep(0.3)
    process.update(1)

resDf.to_excel('原始表咯.xls', index=False)

resDf.rename(columns={'caseTime': '评价时间', 'channelDesc': '评价渠道', 'dealTime': '办结时间', 'evalutionLevel': '评价等级', 'location': '地区', 'matterName': '事项名称', 'name': '差评人姓名', 'raterText': '差评内容', 'reformTime': '整改时间', 'reformer': '整改人', 'statusString': '工单状态', 'departmentName': '部门名称', 'code': '工单编号'}, inplace=True)

resDf = resDf[['工单编号', '地区', '部门名称', '事项名称', '办结时间', '评价时间', '差评内容', '评价渠道', '评价等级', '差评人姓名', '差评人手机', '申诉理由', '驳回理由', '整改回复', '整改人', '工单状态', '追评等级', '追评文本']]

process.close()
resDf.to_excel(f'{arrow.now().strftime("%m%d")}差评信息.xls', index=False)
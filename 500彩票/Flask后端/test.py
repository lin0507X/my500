import time
from datetime import datetime

# start = str(datetime.now())[:16]
# print(start)
# start_cs=int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M")))
# print(start_cs)

# name_stcp=int(time.time())
# print(name_stcp)
# n=time.localtime(name_stcp)
# print(n)
# nn=time.strftime("%Y-%m-%d %H:%M:%S", n)[:16]
# print(nn)
# ss='2022-05-30 23:30'
# print(ss[5:16])

import pymysql

host = 'localhost'
user = 'root'
passwd = '123456'
port = 3306
#
def detection_data():
    db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db='lottery')
    cursor = db.cursor()
    sql = 'select gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange from now_data GROUP BY gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange;'
    cursor.execute(sql)
    res = cursor.fetchall()
    for i in res:
        print(i)
detection_data()

import requests
from lxml import etree

headers = {'User-Agent': 'Baiduspider'}
url='https://odds.500.com/fenxi/ouzhi-1032465.shtml?ctype=2'
def get_data():
    gamestime='2022-05-31 01:00:00'
    # 比赛时间戳
    gamestime_stamp=time.mktime(time.strptime(gamestime, '%Y-%m-%d %H:%M:%S'))
    response=requests.get(headers=headers,url=url)
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    klfc1_3 = []
    klfc2_3 = []
    klfc3_3 = []
    klfc4_3 = []
    klfc5_3 = []
    klfc6_3 = []
    klfc1_1 = []
    klfc2_1 = []
    klfc3_1 = []
    klfc4_1 = []
    klfc5_1 = []
    klfc6_1 = []
    for i in tds:
        update_time = i.xpath('./@data-time')[0]
        update_time_stamp=time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
        # 0<比赛时间-更新时间<=3小时
        if 0<int(gamestime_stamp)-int(update_time_stamp)<=3600*3:
            print(update_time)
            all_data = i.xpath('.//td[3]//@klfc')
            klfc1_3.append(float(all_data[0]))
            klfc2_3.append(float(all_data[1]))
            klfc3_3.append(float(all_data[2]))
            klfc4_3.append(float(all_data[3]))
            klfc5_3.append(float(all_data[4]))
            klfc6_3.append(float(all_data[5]))
        # 0<比赛时间-更新时间<=1小时
        if 0<int(gamestime_stamp)-int(update_time_stamp)<=3600:
            print(update_time)
            all_data = i.xpath('.//td[3]//@klfc')
            klfc1_1.append(float(all_data[0]))
            klfc2_1.append(float(all_data[1]))
            klfc3_1.append(float(all_data[2]))
            klfc4_1.append(float(all_data[3]))
            klfc5_1.append(float(all_data[4]))
            klfc6_1.append(float(all_data[5]))
    if not klfc1_3:
        main_data3 = ''
    else:
        main_data3 = '      '.join([str(i) for i in [round(sum(klfc1_3) / len(klfc1_3), 2),
                                               round(sum(klfc2_3) / len(klfc2_3), 2),
                                               round(sum(klfc3_3) / len(klfc3_3), 2),
                                               round(sum(klfc4_3) / len(klfc4_3), 2),
                                               round(sum(klfc5_3) / len(klfc5_3), 2),
                                               round(sum(klfc6_3) / len(klfc6_3), 2)]])
    if not klfc1_1:
        main_data1 = ''
    else:
        main_data1 = '      '.join([str(i) for i in [round(sum(klfc1_1) / len(klfc1_1), 2),
                                               round(sum(klfc2_1) / len(klfc2_1), 2),
                                               round(sum(klfc3_1) / len(klfc3_1), 2),
                                               round(sum(klfc4_1) / len(klfc4_1), 2),
                                               round(sum(klfc5_1) / len(klfc5_1), 2),
                                               round(sum(klfc6_1) / len(klfc6_1), 2)]])
    print(main_data3,main_data1)
    return (main_data3,main_data1)
# get_data()

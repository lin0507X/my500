import time

import pymysql
from lxml import etree
from datetime import datetime
from saving_data import saving_table, create_db
import requests

host = 'localhost'
user = 'root'
passwd = '123456'
port = 3306

headers = {'User-Agent': 'Baiduspider'}
current_time_ticks = int(time.time())
temp = {}


def get_match_data():
    print('开始爬取----', datetime.now())
    url = 'https://live.500.com/zqdc.php'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except Exception as e:
            print('500彩票列表获取失败，请稍等。。。')
    encode = response.apparent_encoding
    response.encoding = 'GBK'
    html = response.text
    tds = etree.HTML(html).xpath('//table[@id="table_match"]/tbody/tr')
    create_db()
    db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db='lottery')
    cursor = db.cursor()
    for td in tds:
        start = str(datetime.now())  # 当前系统时间
        now_time = start[:11] + '00:00:00'  # 获取当天时间
        now_time_stamp = int(time.mktime(time.strptime(now_time, "%Y-%m-%d %H:%M:%S")))  # 当天时间戳
        try:
            temp['fid'] = td.xpath("@fid")[0]  # 获取比赛id
        except:
            continue
        temp['gamestime'] = ''.join(td.xpath('./td[4]//text()'))  # 比赛时间
        # 比赛时间戳
        games_time = int(time.mktime(time.strptime(('2022-' + temp['gamestime']), "%Y-%m-%d %H:%M")))
        now_state = ''.join(td.xpath('./td[5]/text()'))  # 比赛状态
        # 比赛时间<当天00:00:00+一天零5小时和比赛状态不是结束的话：
        if now_time_stamp <= games_time < now_time_stamp + 104500 and now_state != '完':
            current_now_time = int(time.time())  # 当前时间戳
            # 当前时间-5分钟<比赛时间<=当前时间+5分钟
            if current_now_time - 300 < games_time + 300 <= current_now_time + 300:
                print('比赛开始---------------')
                temp['delayed_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(games_time))[5:16]
                temp['spider_time']=str(datetime.now())[:19]
                temp['home_team'] = ''.join(td.xpath('./td[6]//text()'))  # 主队名
                temp['score'] = ''.join(td.xpath('./td[7]//text()'))  # 比分
                temp['away_team'] = ''.join(td.xpath('./td[8]//text()'))  # 客队名
                delayed_time = temp['delayed_time']
                home_team = temp['home_team']
                away_team = temp['away_team']
                sql1 = f'select * from now_data  where delayed_time="{delayed_time}" and home_team="{home_team}" and away_team="{away_team}";'
                cursor.execute(sql1)
                res = cursor.fetchall()
                if res == ():
                    temp['handicap'] = handicap(temp)
                    temp['All_companies'] = all_companies(temp)
                    temp['BiFa'] = exchange_bifa(temp)
                    temp['Matchbook'] = exchange_Matchbook(temp)
                    temp['Leon'] = exchange_leon(temp)
                    temp['Betsson']=exchange_Betsson(temp)
                    temp['mainstream_companines_3'] = main_compaines(temp)
                    temp['mainstream_companines_1'] = main_compaines_1(temp)
                    temp['Exchange'] = exchange(temp)
                    saving_table(temp)
                else:
                    print('数据存在')

            # # 当前时间-5分钟<比赛时间-1小时<=当前时间+5分钟
            if current_now_time - 300 < games_time - 3600 <= current_now_time + 300:
                print('比赛开始前1小时---------------')
                temp['delayed_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(games_time - 3600))[5:16]
                temp['spider_time']=str(datetime.now())[:19]
                temp['home_team'] = ''.join(td.xpath('./td[6]//text()'))  # 主队名
                temp['score'] = ''.join(td.xpath('./td[7]//text()'))  # 比分
                temp['away_team'] = ''.join(td.xpath('./td[8]//text()'))  # 客队名
                delayed_time = temp['delayed_time']
                home_team = temp['home_team']
                away_team = temp['away_team']
                sql1 = f'select * from now_data  where delayed_time="{delayed_time}" and home_team="{home_team}" and away_team="{away_team}";'
                cursor.execute(sql1)
                res = cursor.fetchall()
                if res == ():
                    temp['handicap'] = handicap(temp)
                    temp['All_companies'] = all_companies(temp)
                    temp['BiFa'] = exchange_bifa(temp)
                    temp['Matchbook'] = exchange_Matchbook(temp)
                    temp['Leon'] = exchange_leon(temp)
                    temp['Betsson']=exchange_Betsson(temp)
                    temp['mainstream_companines_3'] = main_compaines(temp)
                    temp['mainstream_companines_1'] = main_compaines_1(temp)
                    temp['Exchange'] = exchange(temp)
                    saving_table(temp)
                else:
                    print('数据存在')

            # 当前时间-5分钟<比赛时间-3小时<=当前时间+5分钟
            if current_now_time - 300 < games_time - 3600 * 3 <= current_now_time + 300:
                print('比赛开始前3小时---------------')
                temp['delayed_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(games_time - 3600*3))[5:16]
                temp['spider_time']=str(datetime.now())[:19]
                temp['home_team'] = ''.join(td.xpath('./td[6]//text()'))  # 主队名
                temp['score'] = ''.join(td.xpath('./td[7]//text()'))  # 比分
                temp['away_team'] = ''.join(td.xpath('./td[8]//text()'))  # 客队名
                delayed_time = temp['delayed_time']
                home_team = temp['home_team']
                away_team = temp['away_team']
                sql1 = f'select * from now_data  where delayed_time="{delayed_time}" and home_team="{home_team}" and away_team="{away_team}";'
                cursor.execute(sql1)
                res = cursor.fetchall()
                if res == ():
                    temp['handicap'] = handicap(temp)
                    temp['All_companies'] = all_companies(temp)
                    temp['BiFa'] = exchange_bifa(temp)
                    temp['Matchbook'] = exchange_Matchbook(temp)
                    temp['Leon'] = exchange_leon(temp)
                    temp['Betsson']=exchange_Betsson(temp)
                    temp['mainstream_companines_3'] = main_compaines(temp)
                    temp['mainstream_companines_1'] = main_compaines_1(temp)
                    temp['Exchange'] = exchange(temp)
                    saving_table(temp)
                else:
                    print('数据存在')

            # 当前时间-5分钟<比赛时间-5小时<=当前时间+5分钟
            if current_now_time - 300 < games_time - 3600 * 5 <= current_now_time + 300:
                print('比赛开始前5小时---------------')
                temp['delayed_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(games_time - 3600*5))[5:16]
                temp['spider_time']=str(datetime.now())[:19]
                temp['home_team'] = ''.join(td.xpath('./td[6]//text()'))  # 主队名
                temp['score'] = ''.join(td.xpath('./td[7]//text()'))  # 比分
                temp['away_team'] = ''.join(td.xpath('./td[8]//text()'))  # 客队名
                delayed_time = temp['delayed_time']
                home_team = temp['home_team']
                away_team = temp['away_team']
                sql1 = f'select * from now_data  where delayed_time="{delayed_time}" and home_team="{home_team}" and away_team="{away_team}";'
                cursor.execute(sql1)
                res = cursor.fetchall()
                if res == ():
                    temp['handicap'] = handicap(temp)
                    temp['All_companies'] = all_companies(temp)
                    temp['BiFa'] = exchange_bifa(temp)
                    temp['Matchbook'] = exchange_Matchbook(temp)
                    temp['Leon'] = exchange_leon(temp)
                    temp['Betsson']=exchange_Betsson(temp)
                    temp['mainstream_companines_3'] = main_compaines(temp)
                    temp['mainstream_companines_1'] = main_compaines_1(temp)
                    temp['Exchange'] = exchange(temp)
                    saving_table(temp)
                else:
                    print('数据存在')
    print('结束', datetime.now())


# 全部公司了离散值
def all_companies(temp):
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=1'
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break
        except:
            time.sleep(1)
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    data = '      '.join(etree_html.xpath("//td[contains(text(),'离散值')]/../td[2]//tr/td/text()"))
    return data


# Betsson离散值
def exchange_Betsson(temp):
    now_time=int(time.time())
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取Betsson数据失败')
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    update_time=etree_html.xpath('//*[@id="67"]/@data-time')[0]
    update_time_ticks = time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
    if 0<=now_time-update_time_ticks<=3600:
        data = etree_html.xpath('//*[@id="67"]/td[3]/table/tbody/tr/td/@klfc')
        data = '     '.join(data)
    else:
        data=''
    return data

# 必发离散值
def exchange_bifa(temp):
    now_time=int(time.time())
    # 获取必发离散值
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取必发数据失败')
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    update_time=etree_html.xpath('//*[@id="18"]/@data-time')[0]
    update_time_ticks = time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
    if 0<=now_time-update_time_ticks<=3600:
        data = etree_html.xpath('//*[@id="18"]/td[3]/table/tbody/tr/td/@klfc')
        data = '     '.join(data)
    else:
        data=''
    return data


# Matchbook离散值
def exchange_Matchbook(temp):
    now_time=int(time.time())
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取Matchbook离散值数据失败')
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    update_time=etree_html.xpath('//*[@id="142"]/@data-time')[0]
    update_time_ticks = time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
    if 0<=now_time-update_time_ticks<=3600:
        data = etree_html.xpath('//*[@id="142"]/td[3]/table/tbody/tr/td/@klfc')
        data = '      '.join(data)
    else:
        data=''
    return data


# 获取Leon离散值
def exchange_leon(temp):
    now_time=int(time.time())
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取leon数据失败')
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    update_time=etree_html.xpath('//*[@id="1001"]/@data-time')[0]
    update_time_ticks = time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
    if 0<=now_time-update_time_ticks<=3600:
        data = etree_html.xpath('//*[@id="1001"]/td[3]/table/tbody/tr/td/@klfc')
        data = '     '.join(data)
    else:
        data=''
    print(data)
    return data

# # 必发、Matchbook、Leon
# def main_data(temp):
#     # 获取必发离散值
#     url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
#     while True:
#         try:
#             response = requests.get(url, headers=headers)
#             break
#         except:
#             time.sleep(1)
#     response.encoding = 'GBK'
#     result = response.text
#     etree_html = etree.HTML(result)
#     # 必发公司离散值
#     bifa_data = '  '.join(etree_html.xpath("//td[contains(@title,'必发')]/../td[3]//@klfc"))
#     # Matchbook公司离散值
#     Matchbook_data = '   '.join(etree_html.xpath('//*[@id="142"]/td[3]/table/tbody/tr/td/@klfc'))
#     # Leon公司离散值
#     Leon_data = '  '.join(etree_html.xpath('//*[@id="1001"]/td[3]/table/tbody/tr/td/@klfc'))
#     return (bifa_data, Matchbook_data, Leon_data)

# 获取主流公司三小时离散值
def main_compaines(temp):
    competition_time = temp['gamestime']
    competition_time = '2022-' + competition_time + ':00'
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=2'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
    response.encoding = 'GBK'
    klfc1 = []
    klfc2 = []
    klfc3 = []
    klfc4 = []
    klfc5 = []
    klfc6 = []
    result = response.text
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    for td in tds:
        competition_time_ticks = time.mktime(time.strptime(competition_time, '%Y-%m-%d %H:%M:%S'))
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))
        if 0<int(competition_time_ticks) - int(update_time_ticks) <=3600 * 3:
            all_data = td.xpath('.//td[3]//@klfc')
            klfc1.append(float(all_data[0]))
            klfc2.append(float(all_data[1]))
            klfc3.append(float(all_data[2]))
            klfc4.append(float(all_data[3]))
            klfc5.append(float(all_data[4]))
            klfc6.append(float(all_data[5]))
    if not klfc1:
        data = ''
    else:
        data = '      '.join([str(i) for i in [round(sum(klfc1) / len(klfc1), 2),
                                               round(sum(klfc2) / len(klfc2), 2),
                                               round(sum(klfc3) / len(klfc3), 2),
                                               round(sum(klfc4) / len(klfc4), 2),
                                               round(sum(klfc5) / len(klfc5), 2),
                                               round(sum(klfc6) / len(klfc6), 2)]])
    return data

# 获取主流公司一小时离散值
def main_compaines_1(temp):
    competition_time = temp['gamestime']
    competition_time = '2022-' + competition_time + ':00'
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=2'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
    response.encoding = 'GBK'
    klfc1 = []
    klfc2 = []
    klfc3 = []
    klfc4 = []
    klfc5 = []
    klfc6 = []
    result = response.text
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    format = '%Y-%m-%d %H:%M:%S'
    for td in tds:
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, format))
        competition_time_ticks = time.mktime(time.strptime(competition_time, format))
        if 0<int(competition_time_ticks) - int(update_time_ticks) <= 3600:
            all_data = td.xpath('.//td[3]//@klfc')
            klfc1.append(float(all_data[0]))
            klfc2.append(float(all_data[1]))
            klfc3.append(float(all_data[2]))
            klfc4.append(float(all_data[3]))
            klfc5.append(float(all_data[4]))
            klfc6.append(float(all_data[5]))
    if not klfc1:
        data = ''
    else:
        data = '      '.join([str(i) for i in [round(sum(klfc1) / len(klfc1), 2),
                                               round(sum(klfc2) / len(klfc2), 2),
                                               round(sum(klfc3) / len(klfc3), 2),
                                               round(sum(klfc4) / len(klfc4), 2),
                                               round(sum(klfc5) / len(klfc5), 2),
                                               round(sum(klfc6) / len(klfc6), 2)]])
    return data

# 获取交易所两个小时的离散值
def exchange(temp):
    competition_time = temp['gamestime']
    competition_time = '2022-' + competition_time + ':00'
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    global current_time_ticks
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            print('爬取失败')
            time.sleep(1)
    response.encoding = 'GBK'
    klfc1 = []
    klfc2 = []
    klfc3 = []
    klfc4 = []
    klfc5 = []
    klfc6 = []
    result = response.text
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    format = '%Y-%m-%d %H:%M:%S'
    for td in tds:
        competition_time_ticks = time.mktime(time.strptime(competition_time, format))
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, format))
        diff_time = int(competition_time_ticks) - int(update_time_ticks)
        if 0<diff_time <= 3600 * 2:
            all_data = td.xpath('.//td[3]//@klfc')
            klfc1.append(float(all_data[0]))
            klfc2.append(float(all_data[1]))
            klfc3.append(float(all_data[2]))
            klfc4.append(float(all_data[3]))
            klfc5.append(float(all_data[4]))
            klfc6.append(float(all_data[5]))
    if not klfc1:
        data = ''
    else:
        data = '      '.join([str(i) for i in [round(sum(klfc1) / len(klfc1), 2),
                                               round(sum(klfc2) / len(klfc2), 2),
                                               round(sum(klfc3) / len(klfc3), 2),
                                               round(sum(klfc4) / len(klfc4), 2),
                                               round(sum(klfc5) / len(klfc5), 2),
                                               round(sum(klfc6) / len(klfc6), 2)]])
    return data


def handicap(temp):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'referer': 'https://odds.500.com/fenxi/yazhi-920673.shtml',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = f'https://odds.500.com/fenxi1/inc/yazhiajax.php?fid={temp["fid"]}&id=280'
    while True:
        while True:
            try:
                time.sleep(0.5)
                response = requests.get(url, headers=headers)
                break
            except:
                time.sleep(1)
                print('爬取数据失败')
        response.encoding = 'GBK'
        result = response.json()
        try:
            data = '      '.join(etree.HTML(result[0]).xpath('.//text()')).replace('       ', '')
        except:
            data = ''
        return data

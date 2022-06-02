import time
import xlwt
import requests
from lxml import etree
import threading



headers = {'User-Agent': 'Baiduspider'}
current_time_ticks = int(time.time())
temp = {}

def parse_match_list():
    # 获取当前时间
    current_time = time.strftime('%Y-%m-%d %H时%M分', time.localtime())
    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('500彩票')
    list_ = ['time', 'home_team', 'score', 'away_team', 'handicap', 'All_companies',
             'mainstream_companines_3', 'mainstream_companines_1', 'Exchange', 'BiFa', 'Matchbook', 'Leon']
    for i in range(len(list_)):
        sheet.write(0, i, list_[i])
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
    # with open('500.html', mode='w', encoding='GBK') as f:
    #     f.write(html)
    # print('Save ok')
    tds = etree.HTML(html).xpath('//table[@id="table_match"]/tbody/tr')
    line = 0
    clo = 0
    for td in tds:

        try:
            temp['fid'] = td.xpath("@fid")[0]
        except:
            continue
        temp['home_team'] = ''.join(td.xpath('./td[6]//text()'))
        temp['away_team'] = ''.join(td.xpath('./td[8]//text()'))
        temp['handicap'] = handicap(temp)
        temp['time'] = ''.join(td.xpath('./td[4]//text()'))
        temp['score'] = ''.join(td.xpath('./td[7]//text()'))
        # print(temp)
        # try:
        temp['All_companies'] = all_companies(temp)
        temp['mainstream_companines_3'] = main_compaines(temp)
        temp['mainstream_companines_1'] = main_compaines_1(temp)
        temp['Exchange'] = exchange(temp)
        temp['BiFa'] = exchange_bifa(temp)
        temp['Matchbook'] = exchange_Matchbook(temp)
        temp['Leon'] = exchange_leon(temp)
        # except:
        #     continue
        print(temp)
        sheet.write(line + 1, clo, temp['time'])
        sheet.write(line + 1, clo + 1, temp['home_team'])
        sheet.write(line + 1, clo + 2, temp['score'])
        sheet.write(line + 1, clo + 3, temp['away_team'])
        sheet.write(line + 1, clo + 4, temp['handicap'])
        sheet.write(line + 1, clo + 5, temp['All_companies'])
        sheet.write(line + 1, clo + 6, temp['mainstream_companines_3'])
        sheet.write(line + 1, clo + 7, temp['mainstream_companines_1'])
        sheet.write(line + 1, clo + 8, temp['Exchange'])
        sheet.write(line + 1, clo + 9, temp['BiFa'])
        sheet.write(line + 1, clo + 10, temp['Matchbook'])
        sheet.write(line + 1, clo + 11, temp['Leon'])
        work_book.save(f'500彩票-{current_time}.xls')
        line += 1

        print('爬取完成')
        # print(temp['fid'])


# 全部公司了离散值
def all_companies(temp):
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=1'
    while True:
        # 爬取次数
        number = 1
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break
        except:
            time.sleep(1)
            print('全部公司离散值第{}次获取失败'.format(number))
            number += 1
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    data = '      '.join(etree_html.xpath("//td[contains(text(),'离散值')]/../td[2]//tr/td/text()"))
    return data


# 必发离散值
def exchange_bifa(temp):
    # 获取必发离散值
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        number = 1
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('第{}次获取必发数据失败'.format(number))
            number += 1
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    data = etree_html.xpath("//td[contains(@title,'必发')]/../td[3]//@klfc")
    data = '      '.join(data)
    return data


# Matchbook离散值
def exchange_Matchbook(temp):
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        number = 1
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('第{}次获取Matchbook失败'.format(number))
            number += 1
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    data = etree_html.xpath('//*[@id="142"]/td[3]/table/tbody/tr/td/@klfc')
    data = '      '.join(data)
    return data


# 获取Leon离散值
def exchange_leon(temp):
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    while True:
        number = 1
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('第{}次获取leon数据失败'.format(number))
    response.encoding = 'GBK'
    result = response.text
    etree_html = etree.HTML(result)
    data = etree_html.xpath('//*[@id="1001"]/td[3]/table/tbody/tr/td/@klfc')
    data = '     '.join(data)
    return data


# 获取主流公司三小时离散值
def main_compaines(temp):
    competition_time = temp['time']
    competition_time = '2022-' + competition_time+':00'
    # print(competition_time)
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=2'
    while True:
        number = 1
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取主流公司数据第{}次失败'.format(number))
    response.encoding = 'GBK'
    klfc1 = []
    klfc2 = []
    klfc3 = []
    klfc4 = []
    klfc5 = []
    klfc6 = []
    result = response.text
    # print(result)
    # pprint.pprint(result)
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    # print(tds)
    format = '%Y-%m-%d %H:%M:%S'
    for td in tds:
        competition_time_ticks = time.mktime(time.strptime(competition_time, format))
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, format))
        if int(competition_time_ticks) - int(update_time_ticks) >= 3600*3:
            continue
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
    competition_time = temp['time']
    competition_time = '2022-' + competition_time+':00'
    # print(competition_time)
    url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=2'
    while True:
        number = 1
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
            print('获取主流公司数据第{}次失败'.format(number))
    response.encoding = 'GBK'
    klfc1 = []
    klfc2 = []
    klfc3 = []
    klfc4 = []
    klfc5 = []
    klfc6 = []
    result = response.text
    # print(result)
    # pprint.pprint(result)
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    # print(tds)
    format = '%Y-%m-%d %H:%M:%S'
    for td in tds:

        # print(competition_time)
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, format))
        competition_time_ticks = time.mktime(time.strptime(competition_time, format))
        if int(competition_time_ticks) - int(update_time_ticks) >= 3600:
            continue
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
    # print(temp['time'])
    competition_time = temp['time']
    competition_time = '2022-' + competition_time+':00'
    # print(competition_time)
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
    # print(result)
    # pprint.pprint(result)
    etree_html = etree.HTML(result)
    tds = etree_html.xpath('//table[@id="datatb"]/tr')
    # print(tds)
    format = '%Y-%m-%d %H:%M:%S'
    for td in tds:

        competition_time_ticks = time.mktime(time.strptime(competition_time, format))
        update_time = td.xpath('./@data-time')[0]
        update_time_ticks = time.mktime(time.strptime(update_time, format))
        diff_time = int(competition_time_ticks) - int(update_time_ticks)
        if diff_time >= 3600*2:
            continue
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



if __name__ == '__main__':
    start_time = time.time()
    t1 = threading.Thread(target=parse_match_list)
    t1.start()
    end_time = time.time()
    diff_time = end_time - start_time
    print('耗时',diff_time,'秒')
    # parse_match_list()

    # print(all_companies())
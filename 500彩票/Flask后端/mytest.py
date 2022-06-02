import time
from lxml import etree

import requests

headers = {'User-Agent': 'Baiduspider'}

# Betsson离散值
def exchange_Betsson():
    now_time=int(time.time())
    # url = f'https://odds.500.com/fenxi/ouzhi-{temp["fid"]}.shtml?ctype=3'
    url='https://odds.500.com/fenxi/ouzhi-1036321.shtml?ctype=3'
    while True:
        try:
            response = requests.get(url, headers=headers)
            break
        except:
            time.sleep(1)
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
    print(data)
    return data



exchange_Betsson()
import re
import time
from flask import Flask, jsonify, request
from find_data import find_GamesData
from flask_cors import CORS
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from spider import get_match_data

app = Flask(__name__)
app.config['ENV']='development'

CORS(app, supports_credentials=True)
scheduler = APScheduler()
scheduler.init_app(app=app)

scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

# 查询数据
@app.route('/index')
def index():
    url=request.url
    res = re.match('http.*?value.*?=(.*?)T.*?value.*?=(.*?)T', url)
    if res!=None:
        Start_date=time.strftime("%Y-%m-%d",time.localtime(int(time.mktime(time.strptime(res.group(1), "%Y-%m-%d")))+86400))[5:]+' 00:00'
        End_date=time.strftime("%Y-%m-%d",time.localtime(int(time.mktime(time.strptime(res.group(2), "%Y-%m-%d")))+86400))[5:]+' 23:59'
        mytime=[Start_date,End_date]
        myGamesData=find_GamesData(mytime)
    else:
        mytime=[]
        myGamesData=find_GamesData(mytime)
    # return jsonify({'data':myGamesData})
    return jsonify({'data': myGamesData}, {'meta':[{'msg':'查询成功'},{'statu':'200'}]})

# 启动爬虫
@app.route('/startspider')
def startSipder():
    get_match_data()
    return jsonify({'data': '启动成功'}, {'meta':[{'msg':'启动成功'},{'statu':'200'}]})

# 登录
@app.route('/login')
def login():
    return jsonify({'data':{'token':'sdasda'}},{'meta':[{'msg':'登录成功！！！'},{'statu':'200'}]})

scheduler.add_job(func=get_match_data, id='1', trigger='cron', minute ='00,15,30,45')
scheduler.start()
if __name__ == '__main__':
    app.run(debug=False)

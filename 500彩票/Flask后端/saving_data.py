import pymysql

host = 'localhost'
user = 'root'
passwd = '123456'
port = 3306


# 创建数据库
def create_db():
    db = pymysql.connect(host=host, user=user, passwd=passwd, port=port)
    cursor = db.cursor()
    sql = 'create database if not exists lottery default character set utf8'
    cursor.execute(sql)
    db.close()
    create_table()


# 创建数据表
def create_table():
    db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db='lottery')
    cursor = db.cursor()
    sql = 'create table if not exists now_data (fid varchar(255) not null, gamestime varchar(255) not null,delayed_time varchar(255) not null,spider_time varchar(255) null,home_team varchar(255) not null,score varchar(255) not null,away_team varchar(255) not null,handicap varchar(255) not null,All_companies varchar(255) not null,BiFa varchar(255) not null,Matchbook varchar(255) not null,Leon varchar(255) not null,Betsson varchar(255) not null,mainstream_companines_3 varchar(255) not null,mainstream_companines_1 varchar(255) not null,Exchange varchar(255) not null)'
    cursor.execute(sql)
    db.close()


# 保存比赛即时的数据表
def saving_table(srr):
    create_db()
    db = pymysql.connect(host=host, user=user, password=passwd, port=port, db='lottery')
    cursor = db.cursor()
    sql = 'insert into now_data (fid, gamestime,delayed_time, spider_time,home_team,score,away_team,handicap,All_companies, BiFa,Matchbook,Leon,Betsson,mainstream_companines_3,mainstream_companines_1,Exchange) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql, list(srr.values()))
        print(list(srr.values()))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()



import pymysql

host = 'localhost'
user = 'root'
passwd = '123456'
port = 3306



def find_GamesData(mytime):
    db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db='lottery')
    cursor = db.cursor()
    if mytime==[]:
        sql = 'select gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange from now_data GROUP BY gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange ;'
        cursor.execute(sql)
        res = cursor.fetchall()
        mylist=[]
        for i in res:
            mylist.append({'gamestime':i[0],'home_team':i[2],'score':i[3],'away_team':i[4],'handicap':i[5],'All_companies':i[6],'BiFa':i[7],'Matchbook':i[8],'Leon':i[9],'mainstream_companines_3':i[10],'mainstream_companines_1':i[11],'Exchange':i[12]})
        return mylist

    elif mytime!=[]:
        sql = f'select gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange from now_data where  gamestime<="{mytime[1]}" and gamestime>="{mytime[0]}" GROUP BY gamestime,delayed_time,home_team,score,away_team,handicap,All_companies,BiFa,Matchbook,Leon,mainstream_companines_3,mainstream_companines_1,Exchange;'
        cursor.execute(sql)
        res = cursor.fetchall()
        mylist=[]
        for i in res:
            mylist.append({'gamestime':i[0],'home_team':i[2],'score':i[3],'away_team':i[4],'handicap':i[5],'All_companies':i[6],'BiFa':i[7],'Matchbook':i[8],'Leon':i[9],'mainstream_companines_3':i[10],'mainstream_companines_1':i[11],'Exchange':i[12]})
        return mylist
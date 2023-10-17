import pymysql
import time
import random
import datetime

nid = 1
db = pymysql.connect(
                    host = '127.0.0.1' 
                    ,user = 'root' 
                    ,passwd='FvluysbrfsYCDXOC1L1B'
                    ,port= 3306
                    ,db='test_database'
                    ,charset='utf8' 
                    )
cursor = db.cursor()

while (1):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tem = "%.2f" %(random.random() + random.randint(20, 120))
    try:
        sql = "INSERT INTO tempurter (main_time, tem, id) VALUES ('%s', %s, %s)" %(create_time, tem, nid)
        print(create_time, tem, nid)
        nid += 1

        cursor.execute(sql)
        db.commit()

    except:
        print ("Error")
        db.rollback()

    time.sleep(2)
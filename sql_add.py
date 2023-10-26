import pymysql
import time
import random
import datetime

db = pymysql.connect(
                    host = '127.0.0.1' 
                    ,user = 'root' 
                    ,passwd='123456'
                    ,port= 3306
                    ,db='test_database'
                    ,charset='utf8' 
                    )
cursor = db.cursor()

while (1):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tem = "%.2f" %(random.random() + random.randint(20, 120))
    try:
        sql = "INSERT INTO tempurter (main_time, tem, pot_num) VALUES ('%s', %s, 1)" %(create_time, tem)
        cursor.execute(sql)
        db.commit()

    except Exception as e:
        # 如果发生错误，打印错误信息
        print(e)
        db.rollback()

    time.sleep(2)
    
import pymysql


def dateQuery(date):
    dateStatus = '0'
    try:
        conn = pymysql.connect(host='localhost',port=3306,user='weberpython',password='bin2017',db='qqs',charset='utf8')
        cursor = conn.cursor()
        sql0 = 'SELECT status FROM holiday_fw WHERE date = ' + date

        #sql1 = 'INSERT INTO holiday_fw (date, status) VALUES (%s, %s)'
        cursor.execute(sql0)

        status = cursor.fetchone()
        #print(type(status))
        #print('!!!')

        #print(status)

        dateStatus = status[0]

        conn.commit()
        cursor.close()
        conn.close()
        return dateStatus

    except Exception:
        print("error")

    return dateStatus

#print(dateQuery('20170618'))
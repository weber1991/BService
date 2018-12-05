import pymysql



def selectWaitingCountFang():
    sql = "SELECT * FROM showdataFangGuan"
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='weberpython',
        password='bin2017',
        db='qqs',
        charset='utf8'
    )
#   cursor1 = conn.cursor()
#   cursor1.execute(sql1, (str(date2)))
    cursor = conn.cursor()
    cursor.execute(sql)

    wechatData = []
#    data = cursor.fetchall()
#    for i in range(0,len(data)):
#        wechatData.setdefault(i,[]).append(data[i])
    for data_list in cursor.fetchall():
        if data_list is None:
             continue
        else:
            data_one = { }
            data_one['WindowCount'] = data_list[2]
            data_one['WaitingCount'] = data_list[1]
            data_one['ServerName'] = data_list[0]
            wechatData.append(data_one)

    conn.commit()
    cursor.close()
    conn.close()
    return wechatData

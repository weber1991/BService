#-*-coding:utf-8-*-
import pymysql

def selectWaitingCount():
    sql = "SELECT * FROM showdata4 ORDER BY ServiceId"
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
            #print data_list[0]
            data_one['CounterNo'] = data_list[0]
            data_one['ServiceNo'] = data_list[1]
            data_one['ServiceName'] =data_list[2]
            data_one['ServiceId'] = data_list[3]
            data_one['WaitingNumber'] = data_list[4]
            if data_list[5] is None:
                data_one['TicketNo']= '无'
            else:
                data_one['TicketNo'] = data_list[5]
            wechatData.append(data_one)
    conn.commit()
    cursor.close()
    conn.close()
    return wechatData
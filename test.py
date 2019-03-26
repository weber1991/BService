def get_workstate():
    '''
    获取当前的工作状态
    dayState：0，1，2--工作日，法定节假日，节假日补休，休息日
    timeState：0，1，工作时间，非工作时间
    '''
    import json,requests,datetime

    # 先判断工作日再判断时间
    ans = {'timeState':0, 'dayState':0}
    now = datetime.datetime.now()
    dayStr = now.strftime("%Y%m%d")

    APIUrl = 'https://api.goseek.cn/Tools/holiday?date='
    api = APIUrl + dayStr
    req = requests.get(api)
    answer = json.loads(req.text)
    req.close()
    ans['dayState'] = answer['data']

    timeStr = int(now.strftime('%H%M'))
    # 工作时间为8：30-12：00，14：00-17：30
    # 可以用时间模块来比较，但这里直接转换为整数来比较，考虑到提前取号，所以整个时间段为800-1730，

    if (timeStr > 800) and (timeStr < 1730):
        ans['timeState'] = 0
    else:
        ans['timeState'] = 1 
    return ans


if __name__ == "__main__":
    print(get_workstate())
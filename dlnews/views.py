# -*- coding:utf-8 -*-
import logging
from django.shortcuts import render, HttpResponse
import json
import requests

# Create your views here.
dlnewsURL = "http://app.dg.gov.cn/u/port/list?code=dalang&key=6a6d81a922a44afcb4fb0f47a8a1bc55&channel_id=9b211ea848e84b0ab720e1b6cefbd796"


def wechatfile(req):
    return HttpResponse("feaAP9wnuLNU6Xzv")


def dlnews_index(req):
    '''
    获取第一页的新闻并返回到index显示
    :param req:
    :return:新闻序列, 当前页码
    '''
    dlnewsList = getNewsList(1)
    if dlnewsList:
        return render(req,
                      "dlnews/dlnews_index.html",
                      {"dlnewsList": dlnewsList["data"], }
                      )
    else:
        return render(req, "dlnews/dlnews_error.html", {})


def dlnews_show(req):
    '''
    获取新闻详细信息并返回到shownew显示
    :param req:
    :return:
    '''
    newId = req.GET["newId"]
    # print newId
    newUrl = "http://app.dg.gov.cn/u/port/getInfo?id=" + newId
    dlnewJson = requests.get(newUrl).text
    dlnew = json.loads(dlnewJson)
    if dlnew["result"] == '1':
        temp = completeContent(dlnew)
        return render(req, "dlnews/dlnews_show.html", {"dlnew": temp["msg"]})
    else:
        return render(req, "dlnews/dlnews_error.html", {})


def completeContent(dic):
    '''
    将新闻内容的中图片地址补全(/dalang/ to http://dg.gov.cn/dalang/)
    :param dic:新闻接口所获取的json数据
    :return:补全之后的新闻信息
    '''
    temp = dic
    if temp["result"]:
        tempStr = temp["msg"]["content"].replace('/dalang/', 'http://dg.gov.cn/dalang/')
        temp["msg"]["content"] = tempStr
        return temp
    else:
        return temp


def ajax_getmore(req):
    pageCount = int(req.GET["pageCount"])

    if pageCount is not None:
        moreList = getNewsList(pageCount + 1)
        return HttpResponse(json.dumps(moreList["data"]), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


def getNewsList(pageCount):
    '''
    获取某一页码数的新闻序列
    :param pageCount: 页码
    :return:
    '''
    tempUrl = "&curPage=" + str(pageCount)

    dlnewsListJson = requests.get(dlnewsURL + tempUrl)


    dlnewsList = json.loads(dlnewsListJson.text)

    # print "getNewsList result : " + dlnewsList["result"]
    if dlnewsList["result"] == '1':
        return dlnewsList
    else:
        return False

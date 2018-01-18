#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.http import HttpResponse
from django.views.generic import View
import json
from collections import OrderedDict
from blogweb.models import Article,AboutMe,TagInfo,Toys

class getAllArticles(View):
    def get(self, request):
        returndata = {"code":200,"errMsg":"","body":{}}
        try:
            AllCount = Article.objects.filter(status='p').all().count()
            ArticleObjs = Article.objects.filter(status='p').order_by('-id').all()
            returndata['body']['count'] = AllCount
            returndata['body']['articles'] = []
            for i in ArticleObjs:
                articleInfo = {}
                articleInfo['id'] = i.id
                articleInfo['titile'] = i.title
                articleInfo['timestamp'] = i.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                articleInfo['tags'] =  [x.tagname  for x in i.tag.all()]
                articleInfo['url'] = 'http://niubidian.top/blog/show/' + str(i.id) + "/"            
                returndata['body']['articles'].append(articleInfo)
            resp = HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
            return resp
        except:
            returndata["code"] = 400
            returndata["errMsg"] = 'request error'
            return HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
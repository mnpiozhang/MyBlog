#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.http import HttpResponse
from blogweb.popularbooks.getinfo import get_JD_Top
from blogweb.popularbooks import config  as cfg
from django.views.generic import View
import json
from collections import OrderedDict

class jdBooksApi(View):
    '''
    https://niubidian.top/blog/jdbooks/?item=nbs&category=novel&effectivetime=week&topnumber=23
    http://127.0.0.1:8000/blog/jdbooks/?item=nbs&category=novel&effectivetime=week&topnumber=23
    返回的TOP数量可以自己定义1--100
    
    item  str  default 新书销量榜  nbs  
    新书销量榜    nbs  
    图书热评榜    bc
    新书热评榜    nbc
    图书销量榜    bs
    ----------------------------------
    category str default 计算机与互联网  internet
    少儿                       children
    教育                        edu
    小说文学                 novel
    经管                        manage
    励志与成功            jitang
    人文社科                socialscience
    生活                        life
    艺术、摄影            art
    科技                        science
    计算机与互联网       internet
    英文书、港台书        en
    杂志期刊                  magazine
    ----------------------------------
    effectivetime str default 最近24小时 day
    最近24小时  day
    最近一周     week
    最近30天     month
    '''
    def get(self, request):
        returndata = {"code":200,"errMsg":"","body":[]}
        item = request.GET.get('item')
        category = request.GET.get('category')
        effectivetime = request.GET.get('effectivetime')
        try:
            topnumber = int(request.GET.get('topnumber'))
        except:
            returndata["code"] = 400
            returndata["errMsg"] = 'topnumber must be number'
            return HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
        if all([item,category,effectivetime,topnumber]):
            if item not in cfg.ITEM.keys() or category not in cfg.CATEGORY.keys() or effectivetime not in cfg.EFFECTIVE_TIME.keys() or topnumber<=0 or topnumber>100:
                returndata["code"] = 400
                returndata["errMsg"] = 'request error111'
                return HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
            else:
                if effectivetime != 'day' and (item == 'bc' or item == 'nbc'):
                    returndata["code"] = 400
                    returndata["errMsg"] = '热评榜只有24小时内的'
                    return HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
                else:
                    #a is json, like {"top1": {"url": "//item.jd.com/12236229.html", "name": "妖猫传（沙门空海·大唐鬼宴 全四册经典套装）", "pic": "//img13.360buyimg.com/n3/jfs/t12199/194/878683607/225186/13de2d7c/5a15320dNdfbe411e.jpg"}, "top2": {"url": "//item.jd.com/12239650.html", "name": "余华作品：活着", "pic": "//img14.360buyimg.com/n3/jfs/t10162/279/1390942739/246693/50c56f9d/59e02214N37418280.jpg"}}
                    # i want to trans it 
                    a = get_JD_Top(item,category,effectivetime,topnumber)
                    a = json.loads(a,object_pairs_hook = OrderedDict)
                    #print a
                    resultList = []
                    for k,v in a.items():
                        resultList.append({u'rank':k,u'url':v[u'url'],u'name':v[u'name'],u'pic':v[u'pic']})
                    returndata["body"] = resultList
                    resp = HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
                    #resp["Access-Control-Allow-Headers"] = "content-type"
                    #resp["Access-Control-Allow-Origin"] = "*"
                    #resp["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                    #resp["Access-Control-Max-Age"] = "1000"
                    return resp
        else:
            returndata["code"] = 400
            returndata["errMsg"] = 'request error'
            return HttpResponse(json.dumps(returndata,ensure_ascii=False,indent=2),content_type="application/json")
#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.shortcuts import render,render_to_response,redirect
from blogweb.models import Article
from django.template.context import RequestContext
from common  import  Page,page_div
# Create your views here.
def index(request,page):
    ret = {'ArticleObj':None,'PageInfo':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    AllCount = Article.objects.all().count()
    PageObj = Page(AllCount,page)
    ArticleObj = Article.objects.all()[PageObj.begin:PageObj.end]
    pageinfo = page_div(page, PageObj.all_page_count)
    ret['PageInfo'] = pageinfo
    ret['ArticleObj'] = ArticleObj
    
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

def showarticle(request,articleId):
    ret = {'ArticleObj':None}
    ArticleObj = Article.objects.get(id=articleId)
    ret['ArticleObj'] = ArticleObj
    return render_to_response('show.html',ret)
#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.shortcuts import render,render_to_response,redirect
from blogweb.models import Article
from django.template.context import RequestContext
from common  import  Page,page_div,article_div
# Create your views here.
def index(request,page=1):
    ret = {'ArticleObj':None,'PageInfo':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    AllCount = Article.objects.all().count()
    PageObj = Page(AllCount,page,4)
    #更具主键序号倒序排列
    ArticleObj = Article.objects.order_by('-id').all()[PageObj.begin:PageObj.end]
    pageinfo = page_div(page, PageObj.all_page_count)
    ret['PageInfo'] = pageinfo
    ret['ArticleObj'] = ArticleObj
    
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

def showarticle(request,articleId):
    ret = {'ArticleObj':None}
    ArticleObj = Article.objects.get(id=articleId)
    AllCount = Article.objects.all().count()
    #articleId是unicode类型需转成int
    articlecontext = article_div(int(articleId),AllCount)
    ret['ArticleObj'] = ArticleObj
    ret['articlecontext'] = articlecontext
    return render_to_response('show.html',ret,context_instance=RequestContext(request))
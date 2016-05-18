#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.shortcuts import render,render_to_response,redirect
from blogweb.models import Article,AboutMe,TagInfo
from django.template.context import RequestContext
from common  import  Page,page_div,article_div
from collections import OrderedDict
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
    #上一篇的文档对象，由于文档展示排序是倒叙，所以上一篇id正常的未删除任何文章的话就是加一,如果上一篇不存在，则赋值空
    try:
        PreviousArticleObj = Article.objects.order_by('id').filter(id__gt=articleId)[0:1].get()
    except:
        PreviousArticleObj = None
    #下一篇的文档对象，由于文档展示排序是倒叙，所以下一篇id正常的未删除任何文章的话就是减一,如果下一篇不存在，则赋值空
    try:
        NextArticleObj = Article.objects.order_by('-id').filter(id__lt=articleId)[0:1].get()
    except:
        NextArticleObj = None
    #print PreviousArticleObj.id
    #print NextArticleObj.id

    articlecontext = article_div(PreviousArticleObj,NextArticleObj)
    ret['ArticleObj'] = ArticleObj
    ret['articlecontext'] = articlecontext
    return render_to_response('show.html',ret,context_instance=RequestContext(request))

def searchtag(request,tagname):
    ret = {'ArticleObj':None,'PageInfo':None}
    #根据Article对象的tag字段多对多对应TagInfo表的tagname字段
    MatchTagObj = Article.objects.filter(tag__tagname__contains = tagname)
    AllCount = MatchTagObj.all().count()
    #分页为首页
    page = 1
    PageObj = Page(AllCount,page,4)
    ArticleObj = MatchTagObj.order_by('-id').all()[PageObj.begin:PageObj.end]
    pageinfo = page_div(page, PageObj.all_page_count)
    ret['PageInfo'] = pageinfo
    ret['ArticleObj'] = ArticleObj
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

def aboutme(request):
    ret = {'AboutMeObj':None}
    AboutMeObj = AboutMe.objects.get(id=1)
    ret['AboutMeObj'] = AboutMeObj
    return render_to_response('about.html',ret)
    
def archive(request):
    ret = {'ArchiveDict':None}
    tmpArchiveDict = OrderedDict()
    ArticleObjList = []
    ArticleDate = Article.objects.dates('timestamp','month',order='DESC')
    for i in ArticleDate:
        ArticleObj = Article.objects.filter(timestamp__year=i.year).filter(timestamp__month=i.month)
        ArticleObjList.append(ArticleObj)
    #创建有序字典序列
    tmpArchiveDict = OrderedDict(zip(ArticleDate,ArticleObjList))
    print tmpArchiveDict
    ArchiveDict = tmpArchiveDict
    ret['ArchiveDict'] = ArchiveDict
    return render_to_response('archive.html',ret)
    
def tags(request):
    ret = {'taglst':None}
    tagsObj = TagInfo.objects.all()
    taglst = []
    dictemplate = ('tagname','count')
    for i in tagsObj:
            MatchTagObj = Article.objects.filter(tag__tagname__contains = i.tagname)
            MatchTagCount = MatchTagObj.all().count()
            taglst.append(dict(zip(dictemplate,(i.tagname,MatchTagCount))))
    ret['taglst'] = taglst
    #print taglst
    return render_to_response('tags.html',ret)

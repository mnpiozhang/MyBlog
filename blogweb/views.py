#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponseNotFound
from blogweb.models import Article,AboutMe,TagInfo,Toys
from django.template.context import RequestContext
from common  import  Page,page_div,article_div,search_result
from collections import OrderedDict
import popularbooks as pb
import json

# Create your views here.
def index(request,page=1):
    ret = {'ArticleObj':None,'PageInfo':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    AllCount = Article.objects.filter(status='p').all().count()
    PageObj = Page(AllCount,page,6)
    #根据主键序号倒序排列
    ArticleObj = Article.objects.filter(status='p').order_by('-id').all()[PageObj.begin:PageObj.end]
    pageurl = 'index'
    pageinfo = page_div(page, PageObj.all_page_count,pageurl)
    ret['PageInfo'] = pageinfo
    ret['ArticleObj'] = ArticleObj
    
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

def showarticle(request,articleId):
    ret = {'ArticleObj':None}
    #添加是否为草稿的判断,防止直接请求url查看到草稿的文章.
    try:
        ArticleObj = Article.objects.get(id=articleId,status='p')
    except:
        #如果查询出错，含有文章但是文章为草稿或文章id不存在的情况，返回404
        return HttpResponseNotFound('<h1>Page not found</h1>')    
    #上一篇的文档对象，由于文档展示排序是倒叙，所以上一篇id正常的未删除任何文章的话就是加一,如果上一篇不存在，则赋值空
    try:
        PreviousArticleObj = Article.objects.order_by('id').filter(id__gt=articleId,status='p')[0:1].get()
    except:
        PreviousArticleObj = None
    #下一篇的文档对象，由于文档展示排序是倒叙，所以下一篇id正常的未删除任何文章的话就是减一,如果下一篇不存在，则赋值空
    try:
        NextArticleObj = Article.objects.order_by('-id').filter(id__lt=articleId,status='p')[0:1].get()
    except:
        NextArticleObj = None
    #print PreviousArticleObj.id
    #print NextArticleObj.id

    articlecontext = article_div(PreviousArticleObj,NextArticleObj)
    ret['ArticleObj'] = ArticleObj
    ret['articlecontext'] = articlecontext
    return render_to_response('show.html',ret,context_instance=RequestContext(request))

def searchtag(request,tagname,page=1):
    ret = {'ArticleObj':None,'PageInfo':None,'TagName':None}
    #根据Article对象的tag字段多对多对应TagInfo表的tagname字段
    MatchTagObj = Article.objects.filter(tag__tagname__contains = tagname,status='p')
    #判断如果传进来的tagname查不出结果就返回404
    if not MatchTagObj:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    AllCount = MatchTagObj.all().count()
    #分页为首页
    try:
        page = int(page)
    except Exception:
        page = 1
    PageObj = Page(AllCount,page,4)
    ArticleObj = MatchTagObj.order_by('-id').all()[PageObj.begin:PageObj.end]
    pageurl = 'tag' + '/' + tagname
    pageinfo = page_div(page, PageObj.all_page_count,pageurl)
    ret['PageInfo'] = pageinfo
    ret['ArticleObj'] = ArticleObj
    ret['TagName'] = tagname
    return render_to_response('index.html',ret,context_instance=RequestContext(request))

def searchtitle(request):
    if request.method == 'POST':
        search = request.POST.get('search',None)
        if search == "":
            ret = {'Search':None,'Hit':0,'Article':None}
            return render_to_response('search.html',ret,context_instance=RequestContext(request))

        result = search_result(search)
        hitcount = result["hits"]["total"]
        if hitcount == 0:
            ret = {'Search':search,'Hit':0,'Article':None}
        else:
            #重新定义hitcount避免草稿的数量也统计进去.
            #如果搜索hit为1，但是命中的文章为草稿，则hitcount重置为0，无搜索结果
            hitcount = 0
            ArticleLst = []
            for i in result["hits"]["hits"]:
                #判断是否为草稿，草稿直接pass
                if i['_source']['status'] == "p":
                    tmpdict = {}
                    tmpdict['id'] = i['_id']
                    tmpdict['title'] = i['_source']['title']
                    ArticleLst.append(tmpdict)
                    hitcount = hitcount +1
                else:
                    continue
            ret = {'Search':search,'Hit':hitcount,'Article':ArticleLst}
        return render_to_response('search.html',ret,context_instance=RequestContext(request))
    else:
        return redirect('/blog/index')

'''
def searchtitle(request):
    if request.method == 'POST':
        search = request.POST.get('search',None)
        if search == "":
            return redirect('/blog/index')
        ret = {'ArticleObj':None,'PageInfo':None,'Search':None}
        MatchTagObj = Article.objects.filter(title__contains = search,status='p')
        ArticleObj = MatchTagObj.order_by('-id').all()
        if ArticleObj.count() == 0:
            ret['PageInfo'] = "没有搜索结果"
        else:
            ret['PageInfo'] = ""
        ret['ArticleObj'] = ArticleObj
        ret['Search'] = search
        print search_result(search)
        return render_to_response('index.html',ret,context_instance=RequestContext(request))
    return redirect('/blog/index')
'''


def aboutme(request):
    ret = {'AboutMeObj':None}
    try:
        AboutMeObj = AboutMe.objects.get(id=1)
    except:
        AboutMeObj = None
    ret['AboutMeObj'] = AboutMeObj
    return render_to_response('about.html',ret,context_instance=RequestContext(request))
    
def archive(request):
    ret = {'ArchiveDict':None,'ArticleCount':None}
    ArticleObjList = []
    ArticleDate = Article.objects.filter(status='p').dates('timestamp','month',order='DESC')
    for i in ArticleDate:
        ArticleObj = Article.objects.filter(timestamp__year=i.year).filter(timestamp__month=i.month).filter(status='p').order_by('-timestamp')
        ArticleObjList.append(ArticleObj)
    #创建有序字典序列
    ArchiveDict = OrderedDict(zip(ArticleDate,ArticleObjList))
    ret['ArticleCount'] = Article.objects.filter(status='p').count()
    ret['ArchiveDict'] = ArchiveDict
    return render_to_response('archive.html',ret,context_instance=RequestContext(request))
    
def tags(request):
    ret = {'taglst':None}
    tagsObj = TagInfo.objects.all()
    taglst = []
    dictemplate = ('tagname','count')
    for i in tagsObj:
            MatchTagObj = Article.objects.filter(tag__tagname__contains = i.tagname,status='p')
            MatchTagCount = MatchTagObj.all().count()
            taglst.append(dict(zip(dictemplate,(i.tagname,MatchTagCount))))
    ret['taglst'] = taglst
    #print taglst
    return render_to_response('tags.html',ret,context_instance=RequestContext(request))

def toys(request):
    ret = {'toyObj':None}
    toyObj = Toys.objects.all()
    ret['toyObj'] = toyObj
    return render_to_response('toys.html',ret,context_instance=RequestContext(request))

def itPopularBooks(request):
    ret = {'booksdict':None}
    booksTop20 = pb.get_JD_Top20('nbs','internet','day')
    booksTop20Dict = json.loads(booksTop20,object_pairs_hook = OrderedDict)
    ret['booksdict'] = booksTop20Dict
    return render_to_response('popularbooks.html',ret,context_instance=RequestContext(request))

def novelPopularBooks(request):
    ret = {'booksdict':None}
    booksTop20 = pb.get_JD_Top20('nbs','novel','day')
    booksTop20Dict = json.loads(booksTop20,object_pairs_hook = OrderedDict)
    ret['booksdict'] = booksTop20Dict
    return render_to_response('popularbooks.html',ret,context_instance=RequestContext(request))

def flashtime(request):
    return render(request,'flashtime.html')
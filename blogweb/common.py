#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.utils.safestring import mark_safe

class Page:
    def __init__(self,AllCount,current_page,datanum=3):
        '''
        AllCount 所有数据条数  int
        current_page 当前页  int 
        datanum 每个页面展示多少条数据 ，默认3条  int
        '''
        self.DataNum=datanum
        self.AllCount=AllCount
        self.CurrentPage=current_page
        
    #装饰器property将方法装饰为属性
    @property    
    def begin(self):
        return (self.CurrentPage-1)*self.DataNum
    @property
    def end(self):
        return self.CurrentPage*self.DataNum
    @property
    def all_page_count(self):
        #计算分页页面数量，一共有几页，divmod方法返回商和余数的元祖
        all_page = divmod(self.AllCount,self.DataNum)
        if all_page[1] == 0:
            all_page_count = all_page[0]
        else:
            all_page_count = all_page[0]+1
        return all_page_count
        
        
def page_div(page,all_page_count):
    '''
    page 总页面分页
    page 当前页面   int
    all_page_count 总页数 int
    '''
    #初始化页面分页为列表类型
    pagelist = []
    #分页逻辑判断，html标签的列表
    pagelist.append("<a class='pure-button' href='/blog/index/1'>首页</a>")
    if page == 1:
        pagelist.append("<a class='pure-button prev' href=''>上一页</a>")
    else:
        pagelist.append("<a  class='pure-button prev' href='/blog/index/%d'>上一页</a>" %(page-1))
    
    
    #一次展示9个分页
    if all_page_count < 9:
        begin =0
        end =all_page_count
    elif page <5:
        begin =0
        end =9
        #end = page+4 
    elif page > all_page_count-4:
        #begin = page-5
        begin = all_page_count-9
        end = all_page_count    
    else:
        begin = page-5
        end = page+4
    for i in range(begin,end):
        if page == i+1:
            pagelist.append("<a class='pure-button' style='color:red;' href='/blog/index/%d'>%d</a>" %(i+1,i+1))
        else:
            pagelist.append("<a class='pure-button' href='/blog/index/%d'>%d</a>" %(i+1,i+1))
            

    if page == all_page_count:
        pagelist.append("<a class='pure-button next' href=''>下一页</a>")
    else:
        pagelist.append("<a class='pure-button next' href='/blog/index/%d'>下一页</a>" %(page+1))
    pagelist.append("<a class='pure-button' href='/blog/index/%d'>尾页</a>" %(all_page_count))
    #将列表类型的页面转换成字符串并且转义html标签能在前台显示
    return mark_safe(' '.join(pagelist))

def article_div(PreviousArticleObj=None,NextArticleObj=None):
    '''
    article 文章上下篇分页
    PreviousArticleObj 上一篇文章对象  类型queryset
    NextArticleObj 下一篇文章对象  类型queryset
    '''
    #初始化上一篇下一篇文件分页为列表类型
    pagelist = []
    if NextArticleObj == None:
        pagelist.append("<a class='pure-button prev' href='/blog/show/%d'>上一篇</a>" %(PreviousArticleObj.id))
    elif PreviousArticleObj == None:
        pagelist.append("<a class='pure-button next' href='/blog/show/%d'>下一篇</a>" %(NextArticleObj.id))
    else:
        pagelist.append("<a class='pure-button prev' href='/blog/show/%d'>上一篇</a>" %(PreviousArticleObj.id))
        pagelist.append("<a class='pure-button next' href='/blog/show/%d'>下一篇</a>" %(NextArticleObj.id))
    return mark_safe(' '.join(pagelist))

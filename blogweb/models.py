#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.db import models
from common import trans_localdate_format
from common import sync_es

STATUS_CHOICES = (
                  ('d','Draft'),
                  ('p','Published'),
                    )

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 60,verbose_name = u'标题')
    content = models.TextField(verbose_name = u'内容')
    timestamp = models.DateTimeField(auto_now_add = True,verbose_name = u'时间戳')
    last_modified = models.DateTimeField(auto_now = True,verbose_name = u'最后修改时间')
    tag = models.ManyToManyField('TagInfo',blank = True,verbose_name = u'分类标签')
    pic_height=models.PositiveIntegerField(default = 530)
    pic_width=models.PositiveIntegerField(default = 530)
    pic = models.ImageField(upload_to = 'pic/%Y/%m/%d',blank = True,height_field='pic_height', width_field='pic_width')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='d')
    def __unicode__(self):
        return self.title
    
    #overwrite model save method，在保存后同步指定字段信息到elasticsearch里面。
    def save(self, *args, **kwargs):
        super(self.__class__,self).save(*args, **kwargs)
        try:
            esinsert = {}
            esinsert['title'] = self.title
            esinsert['content'] = self.content
            esinsert['status'] = self.status
            esinsert['createtime'] = trans_localdate_format(self.timestamp)
            #print esinsert
            sync_es(esinsert,self.id)
        except Exception,e:
            print e
            print "sync elasticsearch error"
    
class TagInfo(models.Model):
    tagname = models.CharField(max_length = 20,verbose_name = u'标签名称')
    def __unicode__(self):
        return self.tagname
    
    
class AboutMe(models.Model):
    authname = models.CharField(max_length = 20,verbose_name = u'作者名称')
    introduce = models.TextField(blank = True,verbose_name = u'简介')
    def __unicode__(self):
        return self.authname
    
class Toys(models.Model):
    toyname = models.CharField(max_length = 40 ,verbose_name = u'toy栏目名字')
    toyspan = models.CharField(max_length = 20 ,verbose_name = u'toy名字的span')
    toyurl = models.URLField(max_length = 500 ,verbose_name = u'toy名字url')
    createtime = models.DateTimeField(auto_now_add = True,verbose_name = u'创建时间')
    def __unicode__(self):
        return self.toyname
    class meta:
            ordering = ['-createtime']
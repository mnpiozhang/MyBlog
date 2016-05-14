#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 60,verbose_name = u'标题')
    content = models.TextField(verbose_name = u'内容')
    timestamp = models.DateTimeField(auto_now_add = True,verbose_name = u'时间戳')
    tag = models.ManyToManyField('TagInfo',blank = True,verbose_name = u'分类标签')
    def __unicode__(self):
        return self.title
    
class TagInfo(models.Model):
    tagname = models.CharField(max_length = 20,verbose_name = u'标签名称')
    def __unicode__(self):
        return self.tagname
    
    
class AboutMe(models.Model):
    authname = models.CharField(max_length = 20,verbose_name = u'作者名称')
    email = models.EmailField(blank = True,verbose_name = u'邮箱')
    introduce = models.TextField(blank = True,verbose_name = u'简介')
    def __unicode__(self):
        return self.authname
    
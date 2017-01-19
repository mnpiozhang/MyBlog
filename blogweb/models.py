#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.db import models

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
    last_modified.editable = True
    tag = models.ManyToManyField('TagInfo',blank = True,verbose_name = u'分类标签')
    pic_height=models.PositiveIntegerField(default = 530)
    pic_width=models.PositiveIntegerField(default = 530)
    pic = models.ImageField(upload_to = 'pic/%Y/%m/%d',blank = True,height_field='pic_height', width_field='pic_width')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='d')
    def __unicode__(self):
        return self.title
    
class TagInfo(models.Model):
    tagname = models.CharField(max_length = 20,verbose_name = u'标签名称')
    def __unicode__(self):
        return self.tagname
    
    
class AboutMe(models.Model):
    authname = models.CharField(max_length = 20,verbose_name = u'作者名称')
    introduce = models.TextField(blank = True,verbose_name = u'简介')
    def __unicode__(self):
        return self.authname
    
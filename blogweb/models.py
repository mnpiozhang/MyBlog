#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 60)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    tag = models.ManyToManyField('TagInfo',blank = True)
    
    def __unicode__(self):
        return self.title
    
class TagInfo(models.Model):
    tagname = models.CharField(max_length = 20)
    def __unicode__(self):
        return self.tagname
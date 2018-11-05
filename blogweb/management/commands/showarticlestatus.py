#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from django.core.management.base import BaseCommand, CommandError
from blogweb.models import Article,AboutMe,TagInfo,Toys

'''
(virtualenv)  python manage.py showarticlestatus 5
id is 5 , title is django应用部署,status is p
(virtualenv)  python manage.py showarticlestatus 1
id is 1 , title is Hello World！,status is p
(virtualenv)  python manage.py showarticlestatus 2
article id 2 is not exist
'''

class Command(BaseCommand):
    help = 'command show aritcle status'
    def add_arguments(self,parser):
        parser.add_argument("aid",nargs='+',type=int)
    
    def handle(self,*args,**options):
        for i in options['aid']:
            try:
                article = Article.objects.get(id = i)
                self.stdout.write("id is %s , title is %s,status is %s"%(article.id , article.title,article.status))
            except Article.DoesNotExist:
                #raise CommandError('article id %s is not exist'%(i))
                self.stdout.write('article id %s is not exist'%(i))
            #other logical
            
                
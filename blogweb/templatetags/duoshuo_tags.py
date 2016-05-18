# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.template import Library, Node


DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

register = Library()

class DuoshuoCommentsNode(Node):
    def __init__(self,article_id,article_title,short_name=DUOSHUO_SHORT_NAME):
        self.article_id = template.Variable(article_id)
        self.article_title = template.Variable(article_title)
        self.short_name = short_name
        
        
    def render(self, context):
        #根据上下文转换为真实的变量内容
        actual_article_id = self.article_id.resolve(context)        
        actual_article_title = self.article_title.resolve(context)

        code = '''<!-- Duoshuo Comment BEGIN -->
        <div class="ds-thread" data-thread-key="%s" data-title="%s"></div>
        <script type="text/javascript">
        var duoshuoQuery = {short_name:"%s"};
        (function() {
            var ds = document.createElement('script');
            ds.type = 'text/javascript';ds.async = true;
            ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
            ds.charset = 'UTF-8';
            (document.getElementsByTagName('head')[0] 
             || document.getElementsByTagName('body')[0]).appendChild(ds);
        })();
        </script>
        <!-- Duoshuo Comment END -->''' % (actual_article_id,actual_article_title,self.short_name)
        return code
    
def duoshuo_comments(parser, token):
    #print token
    #将文章id号和文章标题作为模版变量传入标签
    short_name,article_id,article_title= token.contents.split()

    if DUOSHUO_SHORT_NAME:
        return DuoshuoCommentsNode(article_id,article_title,DUOSHUO_SHORT_NAME)
    elif len(short_name) == 2:
        return DuoshuoCommentsNode(article_id,article_title,short_name[1])
    else:
        raise template.TemplateSyntaxError, "duoshuo_comments tag takes SHORT_NAME as exactly one argument"
duoshuo_comments = register.tag(duoshuo_comments)

# 生成remote_auth，使用JWT后弃用
# @register.filter
# def remote_auth(value):
#     user = value
#     duoshuo_query = ds_remote_auth(user.id, user.username, user.email)
#     code = '''
#     <script>
#     duoshuoQuery['remote_auth'] = '%s';
#     </script>
#     ''' % duoshuo_query
#     return code
# remote_auth.is_safe = True

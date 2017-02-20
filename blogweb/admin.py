from django.contrib import admin
from models import Article,TagInfo,AboutMe,Toys
from common import sync_es,trans_localdate_format
# Register your models here.

def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 article was"
    else:
        message_bit = "%s articles were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)

#add manual sync to es 
def sync_to_elasticsearch(self, request, queryset):
    for i in queryset:
        try:
            esinsert = {}
            esinsert['title'] = i.title
            esinsert['content'] = i.content
            esinsert['status'] = i.status
            esinsert['createtime'] = trans_localdate_format(i.timestamp)
            #print esinsert
            sync_es(esinsert,i.id)
            self.message_user(request, "sync to elasticsearch successfully.")
        except:
            self.message_user(request, "sync to elasticsearch happen wrong.")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    #ordering = ['title']
    actions = [make_published,sync_to_elasticsearch]
    readonly_fields = ('last_modified','timestamp',)


admin.site.register(Article,ArticleAdmin)
admin.site.register(TagInfo)
admin.site.register(Toys)
admin.site.register(AboutMe)

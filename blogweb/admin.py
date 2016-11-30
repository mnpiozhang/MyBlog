from django.contrib import admin
from models import Article,TagInfo,AboutMe
# Register your models here.

def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 article was"
    else:
        message_bit = "%s articles were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_published]


admin.site.register(Article,ArticleAdmin)
admin.site.register(TagInfo)
admin.site.register(AboutMe)
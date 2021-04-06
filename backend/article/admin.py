from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter

from utils.filters import TitleFilter 
from article.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'visibility', 'created_at', 'modified_at')
    list_filter = (TitleFilter, 'visibility',('created_at', DateFieldListFilter), ('modified_at', DateFieldListFilter))

    #search_fields = ('title',)

    readonly_fields = (
        "created_at",
        "modified_at",
    )




admin.site.register(Article, ArticleAdmin)

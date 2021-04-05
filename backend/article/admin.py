from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter

from utils.filters import InputFilter, EmailFilter, UsernameFilter
from article.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'visibility', 'created_at', 'modified_at')
    list_filter = ('visibility',('created_at', DateFieldListFilter), ('modified_at', DateFieldListFilter))

    #search_fields = ('content',)

    readonly_fields = (
        "created_at",
        "modified_at",
    )



admin.site.register(Article, ArticleAdmin)

from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.db.models import Q

from utils.filters import TitleFilter 
from article.models import Article
from image.models import Image

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'visibility', 'created_at', 'modified_at')
    list_filter = (TitleFilter, 'visibility',('created_at', DateFieldListFilter), ('modified_at', DateFieldListFilter))

    #search_fields = ('title',)

    readonly_fields = (
        "created_at",
        "modified_at",
    )

    search_param = None

    change_form_template = "admin/change_form_article.html"

    '''
    def __init__(self, *args, **kwargs):
        super(ArticleAdmin, self).__init__(*args, **kwargs)
    '''

    # ovveride change view to pass image objects as extra context
    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        labels = request.GET.get('labels', False)
        extra_context['search_param'] = labels
        # search by csv labels
        if labels:
            labels = labels.split(',')
            qs = Q(labels__icontains=labels[0].strip())
            for label in labels[1:]:
                qs |= Q(labels__icontains=label.strip())
            extra_context['images'] = Image.objects.filter(qs)
        else:
            extra_context['images'] = Image.objects.all()

        return super(ArticleAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )



admin.site.register(Article, ArticleAdmin)

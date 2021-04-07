from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.db.models import Q

from utils.filters import TitleFilter 
from article.models import Article
from image.models import Image

from collections import OrderedDict

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'visibility', 'created_at', 'modified_at', 'published',)
    list_filter = (TitleFilter, 'visibility', 'published', ('created_at', DateFieldListFilter), ('modified_at', DateFieldListFilter))

    #search_fields = ('title',)

    # note that the order of actions will be reversed (in get_actions)
    actions=('unpublish_selected','publish_selected',)

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

    def publish_selected(self, request, queryset):
        # change published to true
        count = queryset.update(published=True)
        if count > 1:
            messages.success(request, "Successfully published " + str(count) + " articles.")
        else:
            messages.success(request, "Successfully published " + str(count) + " article.")
    
    publish_selected.short_description = "Publish selected articles"


    def unpublish_selected(self, request, queryset):
        # change published to false
        count = queryset.update(published=False)
        if count > 1:
            messages.success(request, "Successfully unpublished " + str(count) + " articles.")
        else:
            messages.success(request, "Successfully published " + str(count) + " article.")
    
    unpublish_selected.short_description = "Unpublish selected articles"


    def get_actions(self, request):
        actions = super().get_actions(request)
        # reverse the action list so delete comes latest
        actions = OrderedDict(reversed(list(actions.items())))
        return actions

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

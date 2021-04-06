from django.db import models
from ckeditor.fields import RichTextField
from article.enum import Visibility
from django.utils import timezone

class Article(models.Model):
    author = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, default="")
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    links = models.CharField(max_length=1000, blank=True, null=True)
    visibility = models.CharField(max_length=30, choices=Visibility.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.title
    
    # update modified timestamp on save
    def save(self, *args, **kwargs):
        if self.created_at:
            self.modified_at = timezone.now()
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-modified_at', '-created_at']

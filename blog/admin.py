from django.contrib import admin
from django import forms

from codemirror import CodeMirrorTextarea

from blog.models import Post, Tag, Category


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'body': CodeMirrorTextarea(
            )
        }
        exclude = []


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    form = PostAdminForm

    list_display = ('title', 'slug', 'subtitle', 'published', 'date_created', 'date_modified')
    list_filter = ('published', 'date_created',)
    list_editable = ('slug', 'subtitle', 'published',)
    search_fields = ('title', 'slug', 'subtitle', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_created'
    fields = ('published', ('title', 'slug', 'subtitle'), 'body', ('categories', 'tags'), 'feature_image')
    raw_id_fields = ('categories', 'tags', 'feature_image')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
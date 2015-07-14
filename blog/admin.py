from django.contrib import admin
from django import forms

from codemirror import CodeMirrorTextarea

from blog.models import Post, Tag, Category, Link


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

    list_display = ('title', 'slug', 'subtitle', 'go_live_date', 'take_down_date', 'published',)
    list_filter = ('go_live_date', 'take_down_date',)
    list_editable = ('slug', 'subtitle', 'go_live_date', 'take_down_date',)
    search_fields = ('title', 'slug', 'subtitle', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'go_live_date'
    fields = (('go_live_date', 'take_down_date',), ('title', 'slug', 'subtitle'), 'body', ('categories', 'tags'), 'feature_image', 'related_links',)
    raw_id_fields = ('categories', 'tags', 'feature_image', 'related_links',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    model = Link

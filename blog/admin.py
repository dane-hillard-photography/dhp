from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea

from codemirror import CodeMirrorTextarea

from blog.models import Post, Tag, Category, Link


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        widgets = {
            'body': CodeMirrorTextarea(),
            'meta_description': Textarea(),
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
    save_on_top = True

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'subtitle', 'body', 'feature_image',),
        }),
        ('SEO and Relationships', {
            'fields': ('meta_description', 'categories', 'tags', 'related_links',),
        }),
        ('Publishing', {
            'fields': ('go_live_date', 'take_down_date',),
        }),
    )
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

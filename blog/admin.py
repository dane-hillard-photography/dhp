from django.contrib import admin

from blog.models import Post, Tag, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'slug', 'published', 'date_created', 'date_modified')
    list_filter = ('published', 'date_created',)
    list_editable = ('slug', 'published',)
    search_fields = ('title', 'slug', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_created'
    fields = ('published', ('title', 'slug'), 'body', ('categories', 'tags'), 'feature_image')
    raw_id_fields = ('categories', 'tags', 'feature_image')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
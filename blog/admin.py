from django.contrib import admin

from blog.models import Post, Tag, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'slug', 'published', 'date_created', 'date_modified')
    list_filter = ('date_created',)
    list_editable = ('slug', 'published',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
from django.contrib import admin

from blog.models import Post, Tag, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
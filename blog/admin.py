from django.contrib import admin

from blog.models import Post, Tag, Category, Link
from blog.forms import PostAdminForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    form = PostAdminForm

    list_display = (
        "title",
        "slug",
        "subtitle",
        "go_live_date",
        "take_down_date",
        "published",
    )
    list_filter = (
        "go_live_date",
        "take_down_date",
    )
    list_editable = (
        "slug",
        "subtitle",
        "go_live_date",
        "take_down_date",
    )
    search_fields = (
        "title",
        "slug",
        "subtitle",
        "body",
    )
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "go_live_date"
    save_on_top = True

    fieldsets = (
        ("Content", {"fields": ("title", "slug", "subtitle", "body", "feature_image",),}),
        ("SEO and Relationships", {"fields": ("meta_description", "categories", "tags", "related_links",),}),
        ("Publishing", {"fields": ("go_live_date", "take_down_date",),}),
    )
    raw_id_fields = (
        "categories",
        "tags",
        "feature_image",
        "related_links",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    model = Link

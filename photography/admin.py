from django.contrib import admin

from photography.models import Photograph, Album

class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['title', 'description', 'public', 'album']

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'title', 'description']}),
        ('Publishing', {'fields': ['public', 'album', 'user', 'published_date']}),
    ]
    list_display = ('admin_thumbnail', 'title', 'description', 'album', 'size', 'orientation', 'published_date', 'public', 'user', 'uuid')
    list_filter = ('album', 'public',)
    date_hierarchy = 'published_date'
    search_fields = ['title']
    save_on_top = True

class AlbumAdmin(admin.ModelAdmin):
    list_editable = ['sort_order', 'public']

    fieldsets = [
        ('Album Information', {'fields': ['title', 'sort_order']}),
        ('Publishing', {'fields': ['public', 'user', 'published_date']}),
    ]
    list_display = ('title', 'sort_order', 'published_date', 'public', 'user', 'uuid')
    date_hierarcy = 'published_date'

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Album, AlbumAdmin)

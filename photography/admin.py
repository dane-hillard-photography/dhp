from django.contrib import admin

from photography.models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['title', 'description', 'public', 'published_date']

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'title', 'description']}),
        ('Publishing', {'fields': ['public', 'user', 'published_date']}),
    ]
    list_display = (
        'admin_thumbnail',
        'title',
        'description',
        'size',
        'published_date',
        'public',
        'user',
    )

    list_filter = ('public',)
    date_hierarchy = 'published_date'
    search_fields = ['title']
    save_on_top = True

admin.site.register(Photograph, PhotographAdmin)

from django.contrib import admin

from photography.models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['title', 'description',]

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'title', 'description']}),
    ]
    list_display = (
        'admin_thumbnail',
        'title',
        'description',
        'size',
    )

    search_fields = ['title']
    save_on_top = True

admin.site.register(Photograph, PhotographAdmin)

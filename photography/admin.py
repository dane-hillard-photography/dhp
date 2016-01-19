from django.contrib import admin

from photography.models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['alt_text', 'filename']
    fields = ['admin_thumbnail', 'image', 'filename', 'alt_text']
    readonly_fields = ['admin_thumbnail']

    list_display = (
        'admin_thumbnail',
        'filename',
        'alt_text',
        'size',
    )

    search_fields = ['filename', 'alt_text']
    save_on_top = True

admin.site.register(Photograph, PhotographAdmin)

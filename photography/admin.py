from django.contrib import admin

from photography.models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['in_portfolio', 'alt_text', 'filename']
    fields = ['in_portfolio', 'admin_thumbnail', 'image', 'filename', 'alt_text']
    readonly_fields = ['admin_thumbnail']

    list_display = (
        'admin_thumbnail',
        'in_portfolio',
        'filename',
        'alt_text',
        'size',
    )

    search_fields = ['filename', 'alt_text']
    save_on_top = True

admin.site.register(Photograph, PhotographAdmin)

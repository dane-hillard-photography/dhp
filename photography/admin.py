from django.contrib import admin

from photography.models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['alt_text']

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'alt_text']}),
    ]
    list_display = (
        'admin_thumbnail',
        'alt_text',
        'size',
    )

    search_fields = ['alt_text']
    save_on_top = True

admin.site.register(Photograph, PhotographAdmin)

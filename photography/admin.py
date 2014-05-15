from django.contrib import admin
from django import forms

from photography.models import Photograph, Album, Tag, Service

class PhotographAlbumInline(admin.TabularInline):
    model = Album

class PhotographTagInline(admin.TabularInline):
    model = Photograph.tags.through

class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['title', 'description', 'public', 'album']

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'title', 'description']}),
        ('Publishing', {'fields': ['public', 'user', 'published_date']}),
    ]
    inlines = [PhotographAlbumInline, PhotographTagInline]
    list_display = ('admin_thumbnail', 'title', 'description', 'album', 'size', 'orientation', 'published_date', 'public', 'user', 'uuid')
    list_filter = ('album', 'public', 'tags',)
    date_hierarchy = 'published_date'
    search_fields = ['title']
    save_on_top = True

class AlbumAdmin(admin.ModelAdmin):
    list_editable = ['sort_order', 'public']

    fieldsets = [
        ('Album Information', {'fields': ['title', 'sort_order']}),
        ('Publishing', {'fields': ['public', 'user', 'published_date']}),
    ]
    list_display = ('title', 'sort_order', 'photos', 'published_date', 'public', 'user', 'uuid')
    date_hierarcy = 'published_date'

class TagAdmin(admin.ModelAdmin):
    pass

class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Service

class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm

    def admin_price(self, obj):
        return '$' + str(obj.price)
    admin_price.admin_order_field = 'price'
    admin_price.short_description = 'Price'

    list_display = ('title', 'description', 'admin_price')

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)

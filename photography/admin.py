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

    def save_model(self, request, obj, form, change):
        if 'sort_order' in form.changed_data:
            new_order = form.cleaned_data['sort_order']

            current_order = Album.objects.get(pk=obj.id).sort_order
            existing_album = Album.objects.get(sort_order=new_order)

            if existing_album:
                if new_order > current_order:
                    albums = Album.objects.filter(sort_order__lte=new_order, sort_order__gt=current_order)
                    for album in albums:
                        album.sort_order -= 1
                        super(Album, album).save()
                elif new_order < current_order:
                    albums = Album.objects.filter(sort_order__lt=current_order, sort_order__gte=new_order).reverse()
                    for album in albums:
                        album.sort_order += 1
                        super(Album, album).save()

        super(AlbumAdmin, self).save_model(request, obj, form, change)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Album, AlbumAdmin)

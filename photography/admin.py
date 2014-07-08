from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from photography.models import Photograph, Album, PhotoSet

class PhotographAdmin(admin.ModelAdmin):
    list_editable = ['title', 'description', 'public', 'album', 'published_date']

    fieldsets = [
        ('Photograph Information', {'fields': ['image', 'title', 'description']}),
        ('Publishing', {'fields': ['public', 'album', 'user', 'published_date']}),
    ]
    list_display = (
        'admin_thumbnail',
        'title',
        'description',
        'album',
        'size',
        'published_date',
        'public',
        'user',
    )

    list_filter = ('album', 'public',)
    date_hierarchy = 'published_date'
    search_fields = ['title']
    save_on_top = True
    actions = ['create_photo_set_from_photos']
    radio_fields = {'album': admin.VERTICAL}

    def create_photo_set_from_photos(modeladmin, request, queryset):
        ids = ','.join([str(photo_id) for photo_id in queryset.values_list('id', flat=True)])
        add_photoset_url = '{url}?photos={ids}'.format(url=reverse('admin:photography_photoset_add'), ids=ids)
        print add_photoset_url
        return HttpResponseRedirect(add_photoset_url)

class AlbumAdmin(admin.ModelAdmin):
    list_editable = ['sort_order', 'public', 'published_date']

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

class PhotoSetAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoSetAdminForm, self).__init__(*args, **kwargs)
        self.fields['feature_photo'].queryset = self.instance.photos

    class Meta:
        model = PhotoSet
        widgets = {
            'photos': forms.widgets.CheckboxSelectMultiple
        }

class PhotoSetAdmin(admin.ModelAdmin):
    form = PhotoSetAdminForm

    list_editable = ['title', 'slug', 'body', 'published_date']
    list_display = ('feature_photo_thumbnail', 'title', 'slug', 'body', 'published_date')

    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'feature_photo': admin.HORIZONTAL}

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(PhotoSet, PhotoSetAdmin)
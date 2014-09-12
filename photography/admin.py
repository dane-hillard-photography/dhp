from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from photography.models import Photograph, PhotoSet

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
    actions = ['create_photo_set_from_photos']

    def create_photo_set_from_photos(modeladmin, request, queryset):
        ids = ','.join([str(photo_id) for photo_id in queryset.values_list('id', flat=True)])
        add_photoset_url = '{url}?photos={ids}'.format(url=reverse('admin:photography_photoset_add'), ids=ids)
        print add_photoset_url
        return HttpResponseRedirect(add_photoset_url)

class PhotoSetAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoSetAdminForm, self).__init__(*args, **kwargs)
        try:
            PhotoSet.objects.get(pk=self.instance.pk)
            self.fields['feature_photo'].queryset = self.instance.photos
        except PhotoSet.DoesNotExist:
            initial_photo_ids = None
            initial_data = kwargs.get('initial')
            if initial_data:
                initial_photo_ids = initial_data.get('photos')

            if initial_photo_ids:
                self.fields['feature_photo'].queryset = Photograph.objects.filter(id__in=initial_photo_ids)

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
admin.site.register(PhotoSet, PhotoSetAdmin)
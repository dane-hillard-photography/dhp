from django.contrib import admin

from photography.models import Photograph, Album, Tag

class PhotographAlbumInline(admin.TabularInline):
  model = Photograph.albums.through
  admin_order_field = 'title'

class PhotographTagInline(admin.TabularInline):
  model = Photograph.tags.through

class PhotographAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Photograph Information', {'fields': ['title', 'image']}),
    ('Publishing', {'fields': ['public', 'published_date']}),
  ]
  inlines = [PhotographAlbumInline, PhotographTagInline]
  list_display = ('admin_thumbnail', 'title', 'size', 'published_date', 'public', 'user', 'uuid')
  date_hierarchy = 'published_date'
  search_fields = ['title']

  def save_model(self, request, obj, form, change):
    obj.user = request.user
    obj.save()

class AlbumAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Album Information', {'fields': ['title']}),
    ('Publishing', {'fields': ['public', 'published_date']}),
  ]
  list_display = ('title', 'photos', 'published_date', 'public', 'uuid')
  date_hierarcy = 'published_date'
  admin_order_field = 'title'

class TagAdmin(admin.ModelAdmin):
  admin_order_field = 'title'

admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)


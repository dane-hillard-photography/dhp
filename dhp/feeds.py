from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from photography.models import Photograph

class LatestPhotosFeed(Feed):
	title = "Dane Hillard Photography"
	link = "http://www.danehillard.com"
	description = "Some photos"

	def items(self):
		return Photograph.objects.filter(public=True).order_by('-published_date')[:10]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.description

	def item_link(self, item):
		return reverse('photography:photo', args=[item.uuid])



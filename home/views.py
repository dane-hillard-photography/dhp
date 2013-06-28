from django.views import generic

class IndexView(generic.ListView):
  template_name = 'home/index.html'

  def get_queryset(self):
    return None

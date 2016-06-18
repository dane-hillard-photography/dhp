from django.conf.urls import url

from photography.views import PortfolioView


urlpatterns = [
    url(r'^portfolio', PortfolioView.as_view(), name='portfolio'),
]
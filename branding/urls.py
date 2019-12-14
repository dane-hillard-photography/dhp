from django.conf.urls import url

from branding import views

app_name = "branding"

urlpatterns = [
    url(r"^$", views.BrandingView.as_view(), name="branding"),
]

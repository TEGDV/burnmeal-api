from django.urls import path
from website import views as site_views

urlpatterns = [
    path('', site_views.homepage, name="homepage"),
]


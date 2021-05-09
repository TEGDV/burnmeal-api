from django.urls import path
from api import views as api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Here must be exist token generation and refresh, and everything that be related with
# api things as information and docs
urlpatterns = [
    path("register/", api_views.registration),
    path("protected/", api_views.some_protected_view),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

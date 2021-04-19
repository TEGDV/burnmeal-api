from django.urls import path
from api import views as api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", api_views.registration),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

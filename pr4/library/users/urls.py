from django.urls import path
from .views import CustomObtainAuthToken, RegisterUserAPIView

urlpatterns = [
    path('auth/login/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('auth/register/', RegisterUserAPIView.as_view(), name='register'),
]

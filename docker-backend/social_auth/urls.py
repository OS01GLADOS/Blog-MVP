from django.urls import path
import social_auth.views as social_views

urlpatterns = [
    path(
        'google/login',
        social_views.google_login,
        name='api_social_google',
    ),
    path(
        'google/',
        social_views.google_authenticate,
        name='api_social_google',
    ),
]
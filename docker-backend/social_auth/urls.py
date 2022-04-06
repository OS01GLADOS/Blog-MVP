from django.urls import path
import social_auth.views as social_views

urlpatterns = [
    path(
        'google/',
        social_views.google_authentication,
        name='api_social_google',
    ),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import MainPageView, UserLoginView, UserLogoutView, register_view, profile_page_view, create_post_view, \
    detail_post_view

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('register', register_view, name='register'),
    path('profile', profile_page_view, name='profile'),
    path('create_post', create_post_view, name='create_post'),
    path('post/<int:post_id>', detail_post_view, name='post_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

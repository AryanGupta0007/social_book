from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.upload_post, name='add_post'),
    path('settings/', views.settings, name='settings'),
    path('signout/', views.signout, name='signout'),
    path('signout/', views.signout, name='signout'),
    path('like-post/', views.add_likes, name='add_likes'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('follow/', views.follow_user, name='follow'),

]
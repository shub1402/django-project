from django.urls import path
from . import views
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('logout', views.logout_view ,name='logout'),
    path('login', views.login_view ,name='login'),
    path('register', views.register ,name='register'),
    path('about', views.about ,name='about'),
    path('profile/<str:username>', views.profile ,name='profile'),
    path('createPost', views.createPost ,name='createPost'),
    path('updateProfile', views.updateProfile ,name='updateProfile'),
    path('post/<int:post>', views.viewPost ,name='viewPost'),
    path('updatePost/<int:post>', views.updatePost ,name='updatePost'),
    path('disablePost/<int:post>', views.disablePost ,name='disablePost'),
    path('changePassword', views.changePassword ,name='changePassword'),
]
from django.urls import path
from adminapp import views

app_name = 'blog_admin'

urlpatterns = [
path('admin-home', views.home, name='admin_home'),
path('add-post', views.add_post, name='add_post'),
path('check-title-exist', views.check_title_exist, name='check_title_exist'),
path('save-post', views.save_post, name='save_post'),
path('admin-profile', views. admin_profile, name='admin_profile'),
path('edit-profile', views.edit_profile, name='edit_profile'),
path('save-profile', views.save_profile, name='save_profile'),
]
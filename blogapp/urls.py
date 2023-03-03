from django.urls import path
from blogapp import views

app_name = 'blog'

urlpatterns = [
path('', views.index, name='index'),
path('categories', views.categories, name='categories'),
path('categories/tag/<slug:tag_slug>', views.categories, name='post_list_by_tag'),
path('categories/html', views.html, name='html'),
path('categories/css', views.css, name='css'),
path('categories/js', views.js, name='js'),
path('categories/python', views.python, name='python'),
path('categories/django', views.django, name='django'),
path('about', views.about, name='about'),
path('contact', views.contact, name='contact'),
path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
path('share-post/<int:post_id>', views.share_post, name='share_post'),
path('<int:post_id>/comment', views.post_comment, name='post_comment'),
path('login', views.user_login, name='login'),
path('DoLogin', views.DoLogin, name='do_login'),
path('logout', views.user_logout, name='logout'),
]

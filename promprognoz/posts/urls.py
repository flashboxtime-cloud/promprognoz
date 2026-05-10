from django.contrib import admin
from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.post_list, name = 'post_list'),
    path("<int:post_id>/", views.post_detail, name = 'post_detail'),
    path("<int:post_id>/like/", views.add_like, name='add_like'),
    path("<int:post_id>/comment/", views.add_comment, name = 'add_comment')
]

from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('<int:current_page>/', views.entry_list_page, name='entry_list_page'),
    path('<slug:name>/', views.blog_entry, name='blog_entry'),
]


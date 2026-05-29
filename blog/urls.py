from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Dashboard
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/posts/', views.dashboard_posts, name='dashboard_posts'),
    path('dashboard/posts/create/', views.dashboard_post_create, name='dashboard_post_create'),
    path('dashboard/posts/edit/<int:pk>/', views.dashboard_post_edit, name='dashboard_post_edit'),
    path('dashboard/posts/delete/<int:pk>/', views.dashboard_post_delete, name='dashboard_post_delete'),
    path('dashboard/categories/', views.dashboard_categories, name='dashboard_categories'),
    path('dashboard/categories/delete/<int:pk>/', views.dashboard_category_delete, name='dashboard_category_delete'),
    path('dashboard/tags/', views.dashboard_tags, name='dashboard_tags'),
    path('dashboard/tags/delete/<int:pk>/', views.dashboard_tag_delete, name='dashboard_tag_delete'),
    path('dashboard/comments/', views.dashboard_comments, name='dashboard_comments'),
    path('dashboard/comments/approve/<int:pk>/', views.dashboard_comment_approve, name='dashboard_comment_approve'),
    path('dashboard/comments/delete/<int:pk>/', views.dashboard_comment_delete, name='dashboard_comment_delete'),
    path('dashboard/messages/', views.dashboard_messages, name='dashboard_messages'),
    path('dashboard/messages/read/<int:pk>/', views.dashboard_message_read, name='dashboard_message_read'),
]

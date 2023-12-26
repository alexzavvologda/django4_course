"""
URL configuration for NewsStudyRostelecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "news"

urlpatterns = [
    path('', views.index, name='index'),
    # path('news', views.news, name='news'),
    # path('login', views.login, name='login'),

   # path('profil', views.profil, name='profil'),
    # path('content', views.content, name='content'),
    # path('about', views.about, name='about'),


    path('contacts', views.contacts, name='contacts'),


    #path('news/<str:filtr_type>/<str:filtr_val>/', views.news_all, name='news_all'),
    path('news', views.news_all, name='news'),
    # AJAX
    path('search_auto/', views.search_auto, name='search_auto'),
    path('filtr/<str:filtr_type>/<str:filtr_val>/', views.news_filtr, name='filtr'),
    path('news_author/<str:author_id>/', views.news_author, name='news_author'),

    path('singlepost/<int:id>', views.singlepost, name='singlepost'),

    # РЕДАКТИРОВАНИЕ
    path('create_article/', views.create_article, name='create_article'),
    path('edit/<int:pk>/', views.ArticleUpdateView.as_view(), name='edit'),
    path('article-delete-confirm/<int:pk>/', views.ArticleDeleteView.as_view(), name='article-delete-confirm'),
    path('create_cat/', views.CategoryCreateView.as_view(), name='create_cat'),
    path('create_tag/', views.TagCreateView.as_view(), name='create_tag'),

    path('test_ajax/', views.test_ajax, name='test_ajax'),




]

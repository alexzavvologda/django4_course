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
from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('profil', views.index, name='profil'),

    #path('register', views.register, name='register'),
    #path('register', views.CreateUserView.as_view(), name='register'),
    # сделано через дженерик path('register', views.RegisterUser.as_view(), name='register'),
    # сделано через обработку
    path('register', views.RegisterUserScript, name='register'),

    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
   # path('register/<int:id>', views.singlepost, name='register'),
    path('favorites/<int:id>',views.add_to_favorites, name='favorites'),
]



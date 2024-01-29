"""
URL configuration for kyrciapgg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from d
    
    
    jango.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views
import debug_toolbar
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('player_info/', views.player_info, name='player_info'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


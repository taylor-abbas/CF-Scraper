"""CF_Crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls.conf import include
from .views import index, stats, create_problems_api_view, create_submissions_api_view, create_languages_api_view, create_contests_api_view, create_info_api_view

urlpatterns = [
    # path('', index),
    path('stats/', stats),
    path('', index),
    path('stats/api/data/info', create_info_api_view, name="info-api"),
    path('stats/api/data/contests', create_contests_api_view, name="contests-api"),
    path('stats/api/data/submissions',
         create_submissions_api_view, name="submissions-api"),
    path('stats/api/data/lang', create_languages_api_view, name="languages-api"),
    path('stats/api/data/problems', create_problems_api_view, name="problems-api"),
    # path('charts/', charts)
]

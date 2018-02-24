"""

crawler_app URL Configuration.

The urlpatterns list routes URLs to views.

"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('api.urls')), # adds url prefix for the crawler service
    path('admin/', admin.site.urls)
]

"""crawler_app URL Configuration

The `urlpatterns` list routes URLs to views.

"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('api.urls')) # main app includes apis extra URLs
]

"""
The urlpatterns dictionary holds all the URL mappings to the views functions
 of the crawler service. All urls are added to the main crawler_app.
    
"""

from django.conf.urls import url, include
from .views import crawler_service
from .views import root_view
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    # crawler_service view
    url(r'crawler', crawler_service),

    # token authentication view
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

    # welcome view
    url(r'^$', root_view),
]

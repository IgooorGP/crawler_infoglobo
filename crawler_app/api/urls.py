"""
The urlpatterns dictionary holds all the URL mappings to the views functions
 of the crawler service. All urls are added to the main crawler_app.
    
"""

from django.conf.urls import url, include
from .views import crawler_service
from .views import root

urlpatterns = {    
    url(r'crawler', crawler_service), # refactored route (testable)
    url(r'^$', root) # root route just says hello world
}

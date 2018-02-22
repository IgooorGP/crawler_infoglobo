from django.conf.urls import url, include
from .views import crawler_service
from .views import root

urlpatterns = {
    url(r'crawler', crawler_service),
    url(r'^$', root)
}

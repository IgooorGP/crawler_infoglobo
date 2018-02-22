from django.test import TestCase
from .views import crawler_service
import mock

"""
Test cases for the crawler service.

"""

class TestCrawlerService(TestCase):

    def test_crawler_request(self):
        crawler_service = mock.MagicMock(return_value = 3)

        

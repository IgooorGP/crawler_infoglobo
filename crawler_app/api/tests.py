from django.test import TestCase
from django.conf import settings
from .views import crawler_service
from .helper_functions.crawler_functions import *
import os
import unittest

"""
Test cases for the crawler service.

"""
class TestCrawlerService(TestCase):

    def setUp(self):
        """
        Dummy XML file has 3 <item> tags
        """
        
        # parsing fake xml data with 3 <item>
        with open(os.path.join(settings.PROJECT_ROOT, 'test.txt'), 'r') as myfile:
            xml_str = myfile.read().replace('\n', '')
        
        self.channel_root = get_xml_tree(xml_str, node_name='channel') # gets an xml tree which starts at channel node
        
    def test_find_nodes(self):
        """
        Asserts that find_nodes() function finds each node with <item> tag.
        """
        
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')
        
        # asserts 3 <item> tags
        self.assertEqual(3, len(item_nodes))

    def test_get_nodes_data_item(self):
        """
        Asserts <item><title> tag proper reading by function get_nodes_data().

        """
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')

        # for each <item> node, extract each child <title>
        title_data = get_nodes_data(item_nodes, 'title')

        # asserts number of <item> nodes has the same number of <title> tags
        self.assertEqual(len(item_nodes), len(title_data))

        # asserts contents
        self.assertListEqual(title_data, ['Dummy Title 1', 'Dummy Title 2', 'Dummy Title 3'])
                           
    def test_get_nodes_data_link(self):
        """
        Asserts <item><link> tag proper reading by function get_nodes_data().

        """
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')

        # for each <item> node, extract each child <link>
        link_data = get_nodes_data(item_nodes, 'link')

        # asserts number of <item> nodes has the same number of <link> tags
        self.assertEqual(len(item_nodes), len(link_data))

        # asserts contents of <link> tags
        self.assertListEqual(link_data, ['https://dummyitemlink1.html', 'https://dummyitemlink2.html', 'https://dummyitemlink3.html'])

    def test_html_parsing(self):
        # for each <item> node, extract each <description> = HTML strings
        # html_data = get_nodes_data(item_nodes, 'description')
    
        # # requires extra-parsing
        # description_data = parse_html_content(html_data)
        pass
        

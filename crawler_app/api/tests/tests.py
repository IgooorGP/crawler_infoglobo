from django.test import TestCase
from django.conf import settings
from ..views import crawler_service
from ..helper_functions.crawler_functions import *
import os
import unittest

"""
Test cases for the crawler service.

"""
class TestCrawlerService(TestCase):

    def setUp(self):
        """
        Reads test XML file which has 3 <item> tags
        """
        # parsing test xml data with 3 <item>
        with open(settings.BASE_DIR + '/api/tests/xml_test.txt', 'r', encoding='utf-8') as myfile:
            xml_str = myfile.read().replace('\n', '')
        
        self.channel_root = get_xml_tree(xml_str, node_name='channel') # gets an xml tree which starts at channel node
        
    def test_find_nodes(self):
        """
        Asserts that find_nodes() function finds each node with <item> tag.
        """
        
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')

        # asserts only <item> nodes are parsed
        for node in item_nodes:
            self.assertEqual(node.tag, 'item')

    def test_get_nodes_data_item(self):
        """
        Asserts <item><title> tag proper reading by function get_nodes_data().

        """
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')

        # for each <item> node, extract each child <title>
        title_data = get_nodes_data(item_nodes, 'title')

        # asserts all <title> nodes are read properly
        self.assertListEqual(title_data, ['Dummy Title 1', 'Dummy Title 2', 'Dummy Title 3'])
                           
    def test_get_nodes_data_link(self):
        """
        Asserts <item><link> tag proper reading by function get_nodes_data().

        """
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')

        # for each <item> node, extract each child <link>
        link_data = get_nodes_data(item_nodes, 'link')

        # asserts all <link> nodes are read properly
        self.assertListEqual(link_data, ['https://dummyitemlink1.html', 'https://dummyitemlink2.html', 'https://dummyitemlink3.html'])

    def test_html_parsing(self):
        """
        Tests HTML parsing of <item><description> node.

        """
        
        # finds all <item> tags under <channel> node
        item_nodes = find_nodes(self.channel_root, 'item')
        
        # for each <item> node, extract each <description> = HTML strings
        html_data = get_nodes_data(item_nodes, 'description')
    
        # HTML strings requires extra-parsing
        description_data = parse_html_content(html_data)
        
        # each member of description_data is a ANOTHER list that
        # holds all description objects (ItemDescription) for that feed item
        item_1_descriptions = description_data[0]                          # gets all ItemDescripition objects for first <item> node
        item_1_types = [description.type for description in item_1_descriptions]         # gets all description types for first <item>
        item_1_contents = [description.content for description in item_1_descriptions]   # gets all description contents for first<item>
        
        # expected ItemDescription.types for the first <item><description> html
        expected_types = ['image', 'text', 'text', 'links']

        # expected ItemDescription.contents for the first <item><description> html
        expected_contents = ['https://imgsrc1.com', 'bla1 bla bla blastrong blastrong, bla bla bla a blaanchor mais blabla',
                             'bla2 bla bla blastrong blastrong, bla bla bla a blaanchor mais blabla',
                             ['http://saibamais1.com', 'http://saibamais2.com']]        

        self.assertEqual(item_1_types, expected_types)
        self.assertEqual(item_1_contents, expected_contents)

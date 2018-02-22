from django.http import HttpResponse
from ..models import MyHTMLParser
from ..models import Feed
from ..models import FeedItem
from ..models import Item
from ..models import ItemDescription

import xml.etree.ElementTree as ET
import jsonpickle
import requests

# jsonpickle config
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False);

def get_xml_string(xml_url_source):
    # sends HTTP GET to extract a raw XML string
    r = requests.get(xml_url_source)

    # returns raw sml string to be processed
    return r.text

def get_xml_tree(xml_str, node_name=None):
    """
    Takes an xml_str and parses it into an xml tree data structure.
    By default, returns a reference to the root node but allows an xml tag
    name to be searched in the tree and returned as if it were the root.

    """
    # creates an instance of the XML parser to parse the raw XML string
    # instance begins at the root of the XML tree
    root = ET.fromstring(xml_str)

    if (node_name is None):
        return root
    else:
        # returns None if the desired node was not found
        # in the xml structure
        return root.find(node_name)

    
def find_nodes(root, tag):
    children_nodes = []
    
    # searches for children with the given tag name
    for child in root.findall(tag):
        children_nodes.append(child)

    return children_nodes

def get_nodes_data(nodes, tag):
    data = []
    
    # process each <item>
    for child in nodes:
        data.append(child.find(tag).text)

    return data

def parse_html_content(html_lst):
    """
    Returns description list.

    """
    parserHTML = MyHTMLParser()
    item_descriptions = []
    
    for html_str in html_lst:
        # feeds html str content into the customized parser
        # to extract descriptions
        parserHTML.feed(html_str)

        # retrieve description data objects store in the parser
        # this also resets the parser for next iterations
        item_descriptions.append(parserHTML.get_item_descriptions())
        
    return item_descriptions

def get_feed(title_data, link_data, description_data):
    """
    Combines <title>, <link>, <description> for each <item> node
    to create a list of feed items.

    """    
    size = len(title_data)
    f = Feed([])
    
    for i in range(0, size):
        # creates feed item
        feed_item = FeedItem(title_data[i], link_data[i], description_data[i])
        
        # creates wrapper on top of feed item (just for JSON output)
        item = Item(feed_item)

        # appends new item to feed list
        f.feed.append(item)

    # returns feed
    return f 

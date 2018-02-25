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
    """
    Sends an HTTP GET to an URL to get an XML string.

    """
    
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

    # if a node name_name is given, it is set to be the root of the subtree
    if (node_name is None):
        return root
    else:
        # returns None if the desired node was not found
        # in the xml structure
        return root.find(node_name)
    
def find_nodes(root, tag):
    """
    Takes a root reference to an xml tree and a tag name to build
    a list with all the chidren nodes of the root that matches the tagname

    As an example, if the root is the <channel> node and tag = item, it will return
    a list of references of each <item> tag under the <channel> node.

    """     
    children_nodes = []
    
    # searches for children with the given tag name
    for child in root.findall(tag):
        children_nodes.append(child)

    return children_nodes

def get_nodes_data(nodes, tag):
    """
    Takes a list of references to xml nodes and a tag to build a list with the content
    of each tag that is under the node reference.

    As an example, if nodes = a list of <item> nodes and tag = 'title', the function
    will build a list with all <title> tags for every <item> node in the nodes list.

    """    
    data = []
    
    # process each <item>
    for child in nodes:
        data.append(child.find(tag).text)

    return data

def parse_html_content(html_lst):
    """
    Takes a list of raw HTML strings (each <description> tag under each <item> node)
    and parses it by creating a list that holds lists of ItemDescription objects.

    As an example, if html_list has HTML text for every <item><description> node, the function will
    create a list for each <item> node holding all the descriptions objects.
    
    """
    parserHTML = MyHTMLParser() # instantiates the customized parser
    item_descriptions = []      # list that will hold a list for every <item> node
    
    for html_str in html_lst:
        # feeds html str content into the customized parser to extract descriptions
        parserHTML.feed(html_str)

        # retrieves the description data objects stored in the parser
        # which returns a list of ItemDescription objects
        item_descriptions.append(parserHTML.get_item_descriptions())

    # returns the list of lists
    return item_descriptions

def get_feed(title_data, link_data, description_data):
    """
    Combines <title>, <link>, <description> for each <item> node
    to create a list of feed items.

    title_data       = list of every <item><title> node
    link_data        = list of every <item><link> node
    description_data = list of every <item><description> node (list of lists)

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

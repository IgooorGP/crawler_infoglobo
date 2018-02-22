"""
This file contains all view functions that are used to handle
the HTTP requests to their mapped URLs.

"""
from .helper_functions.crawler_functions import *

def root(request):
    """
    Root route. Returns dummy string text.
    
    """
    return HttpResponse("Hello World!")

def crawler_service(request):
    """
    Crawler service to parse the XML with the latest news of AutoEsporte's magazine and
    return a JSON with all the items from the feed.

    @return JSON containing all news of the feed.

    """
    url          = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'  # url of the feed source
    xml_string   = get_xml_string(url)                                         # gets a raw xml string
    channel_root = get_xml_tree(xml_string, node_name='channel')               # gets an xml tree which starts at channel node
    
    # finds all <item> tags under <channel> node
    item_nodes = find_nodes(channel_root, 'item')
    
    # for each <item> node, extract each child <title>
    title_data = get_nodes_data(item_nodes, 'title')
    
    # for each <item> node, extract each child <link>
    link_data = get_nodes_data(item_nodes, 'link')
    
    # for each <item> node, extract each <description> = HTML strings
    html_data = get_nodes_data(item_nodes, 'description')

    # requires extra-parsing
    description_data = parse_html_content(html_data)

    # get feed wth all data of the latest posts
    feed = get_feed(title_data, link_data, description_data)
    
    # returns JSON 
    return HttpResponse(jsonpickle.encode(feed, unpicklable=False), 'application/json')

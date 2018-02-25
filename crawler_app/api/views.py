"""
This file contains all view functions that are used to handle
the HTTP requests to their mapped URLs.

"""
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .helper_functions.crawler_functions import *

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@permission_classes((AllowAny,))
def root_view(request):
    """
    Root of the api. Sends a welcome JSON to the user. Only for HTTP GET and requires
    no authentication token in the HTTP headers.

    """
    return Response({'Crawler service' : 'Welcome user! Dont forget to login to use the service.'},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated, )) # requires authentication token
def crawler_service(request):
    """
    Crawler service to parse the XML with the latest news of AutoEsporte's magazine and
    return a JSON with all the items from the feed. Only for HTTP GET and REQUIRES
    an authentication token in the HTTP header.

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

    # HTML strings requires extra-parsing to create
    # ItemDescription objects with all content of the <item><description> node
    description_data = parse_html_content(html_data)

    # builds a feed with the parsed <title>, <link> and <description> data
    feed = get_feed(title_data, link_data, description_data)
    
    # returns the JSON 
    return HttpResponse(jsonpickle.encode(feed, unpicklable=False),
                        'application/json', status=status.HTTP_200_OK)

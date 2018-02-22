"""
This file contains all view functions that are used to handle
the HTTP requests to their mapped URLs.

"""

from django.http import HttpResponse
from .models import MyHTMLParser
from .models import Feed
from .models import FeedItem
from .models import Item
from .models import ItemDescription

import xml.etree.ElementTree as ET
import jsonpickle
import requests

# jsonpickle config
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False);

def root(request):
    """
    Root route
    
    """
    return HttpResponse("Hello World!")

def crawler_service(request):
    """
    Crawler service function that parses the XML file with the latest news
    of AutoEsporte's magazine from the following url:

    http://revistaautoesporte.globo.com/rss/ultimas/feed.xml
    
    """

    # instantiates an HTML parser for the <description> node of the XML file
    parserHTML = MyHTMLParser()

    # sends HTTP GET to extract a raw XML string
    r = requests.get('http://revistaautoesporte.globo.com/rss/ultimas/feed.xml')

    # creates an instance of the XML parser to parse the raw XML string
    # instance begins at the root of the XML tree
    root = ET.fromstring(r.text)

    # finds XML node <channel> which contains all important info
    channel_node = root.find('channel')

    # instantiates a custom feed object to store a list of feed item objects
    f = Feed([])
    
    # traverses all nodes of <channel> to get all <item> nodes
    for node in channel_node:
        
        # finds <item> node
        if (node.tag == 'item'):
            # local variable to store <item><title> and <item><link>
            item_title = ''
            item_link = '' 
            
            # traverses the children of <item> node: <title>, <description> and <link>
            for child in node:
                # gets data from <item><title> node
                if (child.tag == 'title'):
                    item_title = child.text

                # gets data from <item><description> node
                if (child.tag == 'description'):
                    html_code = child.text
                    
                    # <description> contains <![CDATA[...]]> which is parsed by the XML parser as an HTML string
                    # uses the HTML parser instance to read the HTML string
                    parserHTML.feed(html_code)
                    
                    # test for feeds that do not end with div to stop text reading
                    # (e.g., feeds that do not end with saibamais div)

                    # trims whitespaces and non-breaking spaces
                    # parserHTML.txt = parserHTML.txt.strip()
                    
                    # if (parserHTML.txt.strip() != ''):                        
                    #     # appends final paragraph of the text reading
                    #     parserHTML.item_descriptions.append(parserHTML.txt)

                    #     # resets variable for next <item> nodes
                    #     parserHTML.txt = ''
                        
                # gets data from <item><link>
                if (child.tag == 'link'):
                    item_link = child.text

            # after traversing the children <link>, <title> and <description> in <item> node
            # it creates a new FeedItem object with a title, its links and a description list with type and value
            feed_item = FeedItem(item_title, item_link, parserHTML.get_item_descriptions())
            
            # creates an Item object on top of FeedItem object (just a wrapper for the correct JSON output)
            item = Item(feed_item)
            
            # appends Item object to the feed list
            f.feed.append(item)

    # builds the JSON response from the object f (Feed object which holds all FeedItems and ItemDescriptions)
    # and returns it
    return HttpResponse(jsonpickle.encode(f, unpicklable=False), 'application/json')

from django.shortcuts import render
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
    parser = MyHTMLParser()
    r = requests.get('http://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
    root = ET.fromstring(r.text)

    # finds xml node <channel>
    channel_node = root.find('channel')

    # feed object
    f = Feed([])
    
    # traverses <channel> node
    for node in channel_node:
        # finds item node
        if (node.tag == 'item'):
            item_title = ''
            item_link = '' 
            
            # traverses children in item node: <title>, <description> and <link>
            for child in node:
                if (child.tag == 'title'):
                    item_title = child.text

                if (child.tag == 'description'):
                    html_code = child.text
                    
                    # description contains raw HTML data which needs extra parsing
                    parser.feed(html_code)
                    
                    # test for feeds that do not end with div to stop text reading
                    # (e.g., feeds that do not end with saibamais div)

                    # trims whitespaces and non-breaking spaces
                    parser.txt = parser.txt.strip()
                    
                    if (parser.txt.strip() != ''):                        
                        # appends final paragraph of the text reading
                        parser.item_descriptions.append(parser.txt)

                        # resets variable for next <item> nodes
                        parser.txt = ''

                if (child.tag == 'link'):
                    item_link = child.text

            # after traversing the children in <item> node, creates a new feed item object         
            feed_item = FeedItem(item_title, item_link, parser.get_item_descriptions())
            
            # creates item object (wrapper for the correct JSON output)
            item = Item(feed_item)
            
            # appends object to the feed list
            f.feed.append(item)

    # final JSON response
    return HttpResponse(jsonpickle.encode(f, unpicklable=False), 'application/json')

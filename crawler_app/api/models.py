from django.db import models
from html.parser import HTMLParser
import re

# docker run -it -p 8000:8000 -p 5858:5858 crawler_app_container
# docker build -t crawler_app_container .

class Feed (object):    
    def __init__(self, feedItemList):
        self.feed = feedItemList # list of FeedItems

class Item(object):
    def __init__(self, feedItem):
        self.item = feedItem

class FeedItem(object):    
    def __init__(self, title, link, description):
        self.title = title             # title of the feed item
        self.link = link               # link of the feed item
        self.description = description # list of contents of the feed item

class ItemDescription (object):    
    def __init__(self, type, content):
        self.type = type       # text, links, image
        self.content = content # string or list of links

class MyHTMLParser(HTMLParser):    
    def __init__(self):
         # super class constructor
         HTMLParser.__init__(self)
      
         # creation of FeedItem with ItemDescription (list)
         self.item_descriptions = []
      
         # instance variables to store data
         self.txt = ''
         self.imgs = []
         self.links = []
        
         # flags for parsing html
         self.is_reading_txt = False
         self.is_reading_saibamais = False

    def handle_starttag(self, tag, attrs):
        if (tag == 'p'):
            self.is_reading_txt = True
            
        if (tag == 'img'):
            # gets img src
            for attribute, value in attrs:
                if (attribute == 'src'):
                    self.stop_reading_img(value)

        # finds a div with saibamais class to extract the links
        if (tag == 'div'):
            # stops reading paragraph text once a div is found (div/img or div/ul)
            self.stop_reading_text()

            for attribute, value in attrs:
                if (attribute == 'class' and 'saibamais' in value):
                    # is reading saibamais div
                    self.is_reading_saibamais = True

        # finds all anchor tags inside saibamais to extract the links
        if (self.is_reading_saibamais and tag == 'a'):
            for attribute, value in attrs:
                if (attribute == 'href'):
                    self.links.append(value)
                    
    def handle_endtag(self, tag):
        # reading saibamais div is over
        if (self.is_reading_saibamais and tag == 'div'):
            self.stop_reading_saibamais()

    def handle_data(self, data):
        # paragraph parsing
        if (self.is_reading_txt):
            data = re.sub('[\t\n]', '', data)
            data = re.sub('\"', '', data)
            
            if (data == ''):
                pass
            else:
                self.txt += (' ' + data.strip())
                
    def stop_reading_text(self):
        # stops paragraph reading
        self.is_reading_txt = False 

        # trims any remaining whitespaces
        self.txt = self.txt.strip()
        
        # if text is empty ignore it
        if (self.txt == ''):            
            pass
        else:
            # creates new description object (text type)
            item_description = ItemDescription('text', self.txt)
        
            # cleans txt instance variable for next paragraphs
            self.txt = ''
        
            # appends new description object
            self.item_descriptions.append(item_description)

    def stop_reading_img(self, src):
        # creates new description object (img type)
        item_description = ItemDescription('image', src)

        # appends new description object
        self.item_descriptions.append(item_description)

    def stop_reading_saibamais(self):
        # stops saibamais reading
        self.is_reading_saibamais = False
      
        # creates new description object (links type)
        item_description = ItemDescription('links', self.links)
        
        # cleans links instance variable for next items
        self.links = []

        # cleans self.txt too against final non-breaking spaces <p>&nbsp;</p>
        self.txt = ''
        
        # appends new description object 
        self.item_descriptions.append(item_description)
      
    def get_item_descriptions(self):
        item_descriptions = self.item_descriptions
        self.item_descriptions = []
        
        return item_descriptions



"""
This file contains all the class definitions required by the
crawler web service.

"""

from django.db import models
from html.parser import HTMLParser
import re

class Feed (object):
    """
    This class represents the whole feed with all the <item> nodes or
    all the latest news of the AutoEsporte magazine. Used to create
    the final JSON.

    """    
    
    def __init__(self, feedItemList):
        self.feed = feedItemList # list of FeedItems

class Item(object):
    """
    This class is wrapper on top of the FeedItem and is just used
    to create the final JSON with the appropriate structure which
    contains an "item" field.

    """    
    
    def __init__(self, feedItem):
        self.item = feedItem # just points to a feedItem for JSON structure only

class FeedItem(object):
    """
    This class represents an <item> node of the XML which is a single
    new from the AutoEsporte magazine. Used to create the final JSON.

    """    
    
    def __init__(self, title, link, description):
        self.title = title             # title of the feed item
        self.link = link               # link of the feed item
        self.description = description # list of contents of the feed item

class ItemDescription (object):
    """
    This class represents an item description object which holds
    two instance variables: type of the content and its value.
    Used to create final JSON.

    """    
    def __init__(self, type, content):
        self.type = type       # text, links, image
        self.content = content # string or list of links

class MyHTMLParser(HTMLParser):
    """
    This class is a customized subclass of the HTMLParser which contains
    overriden methods and new ones in order to parse properly the HTML part
    of the XML file of the magazine.

    """
    
    def __init__(self):
        """
        Default constructor of the class.

        """
        # invokes superclass constructor
        HTMLParser.__init__(self)
            
        # instance variables to store parsing data (no encapsulation)         
        self.txt               = '' # string to concatenate info of the paragraphs <p>
        # self.imgs              = [] # list to hold <img> src attribute
        self.links             = [] # list to hold saibamais <a> links
        self.item_descriptions = [] # creates a list of ItemDescription objects for each article of the website
        
        # sets initial flags for parsing the HTML
        self.is_reading_txt       = False   # indicates that the parser is reading a <p>
        self.is_reading_saibamais = False   # indicates that the parser is reading <div class='saibamais'>

    def handle_starttag(self, tag, attrs):
        """
        Method is invoked when an opening HTML tag is found (e.g., <p>).
        
        @argument tag is a string that holds the name of the tag (e.g. p).
        @argument attrs is list with nested tuples which holds attributes of HTML tags and its values
        as follows: [(attribute, value), (attribute2, value2), ...].

        """
        # parser has found a start tag <p>
        # sets flag to indicate that <p> is being read
        if (tag == 'p'):
            self.is_reading_txt = True
            
        # parser has found an <img>
        if (tag == 'img'):
            
            # unpacks attributes and values of the <img> until the src attribute is found
            for attribute, value in attrs:
                if (attribute == 'src'):
                    # executes method to stop reading <img> and store src tag value
                    self.stop_reading_img(value)

        # parser has found a <div>
        if (tag == 'div'):
            # stops reading paragraph text once a div is found (<div>/<img> or <div>/<ul> - saibamais)
            ###  self.stop_reading_text()

            # unpacks attributes and values of the <div> until the 'saibamais' is found
            for attribute, value in attrs:
                if (attribute == 'class' and 'saibamais' in value):
                    # sets a flag to indicate <div> saibamais is being read
                    self.is_reading_saibamais = True
                
        # if <div> saibamais is being read, finds all anchor tags inside to get the links
        if (self.is_reading_saibamais and tag == 'a'):
            
            for attribute, value in attrs:
                if (attribute == 'href'):
                    # appends the links to the instance variable
                    self.links.append(value)
                    
    def handle_endtag(self, tag):
        """
        Method is invoked when a closing HTML tag is found (e.g., </p>).
        
        @argument tag is a string that holds the name of the closing tag (e.g. p).

        """
        if (tag == 'p'):
            # stops reading the paragraph and stores its content
            self.stop_reading_text()
        
        # if reading saibamais and the closing </div> is found
        if (self.is_reading_saibamais and tag == 'div'):
            # stops reading the <div> and stores the links found
            self.stop_reading_saibamais()

    def handle_data(self, data):
        """
        Method is invoked to read the content of an HTML tag after the start tag has been found.
        Used to extract the content of <p> and all other tags (<a>, <strong) that may be inside
        the paragraph. All text is concatenated to the self.txt variable until stop_reading_text
        function is invoked which sets is_reading_txt flag to False.
        
        @argument data holds the content of the HTML tag.

        """

        # if a start <p> was found, a paragraph is being read
        if (self.is_reading_txt):
            # removes \t and \n character that are parsed as printable characters
            # (e.g., '\t\nfoo' --> 'foo'
            data = re.sub('[\t\n]', '', data)
            
            # removes \" character
            data = re.sub('\"', '', data)

            # ignore empty contents
            if (data == ''):
                pass
            else:
                # appends paragraph content to the instance variable
                # trims unnecessary left/right whitespace and non-breaking spaces (&nbps;)
                self.txt += (' ' + data.strip())
                
    def stop_reading_text(self):
        """
        Method is invoked when a closing </p> is found. It removes whitespaces and
        HTML non-breaking spaces (&nbsp;) from the paragraph content. If the content
        is not null, it creates and a appends a new ItemDescription instance (type text)
        to the item_descriptions list. Resets is_reading_text flag to False.

        """        
        # stops paragraph reading <p>
        self.is_reading_txt = False 

        # trims any remaining whitespaces
        self.txt = self.txt.strip()
        
        # if the content of the paragraph is empty, ignore it
        if (self.txt == ''):            
            pass
        # otherwise,
        else:
            # creates a new description object (text type)
            item_description = ItemDescription('text', self.txt)
            
            # cleans txt instance variable for next <p> tags
            self.txt = ''
        
            # appends new description object of type text with the <p> content
            self.item_descriptions.append(item_description)

    def stop_reading_img(self, src):
        """
        Method is invoked when the <img> src attribute has been captured by the parser.
        The src string is used to create a new ItemDescription instance (type img) and
        appends it to the self.item_descriptions list.

        @argument src is the img src found by the parser.

        """        
        
        # creates new description object
        item_description = ItemDescription('image', src)

        # appends new description object of type image with <img> src attribute content
        self.item_descriptions.append(item_description)

    def stop_reading_saibamais(self):
        """
        Method is invoked when the closing ta </div> of a <div class='saibamais'> is found.
        All the links stored in the self.links list is used to create an ItemDescription
        instance (type links) and is appended to the self.item_descriptions list.

        """        
        # stops <div> saibamais reading
        self.is_reading_saibamais = False
      
        # creates new description object (links type)
        item_description = ItemDescription('links', self.links)
        
        # cleans links instance variable for next <item> node
        self.links = []

        # cleans self.txt too against final non-breaking spaces <p>&nbsp;</p>
        ### self.txt = ''
        
        # appends new description object of type links with <div><a> content
        self.item_descriptions.append(item_description)
      
    def get_item_descriptions(self):
        """
        Method is invoked to get all the ItemDescription objects of the current
        <item> node of the XML parser.

        @return item_descriptions is a list with all the description objects for
        this <item> node.

        """                
        item_descriptions = self.item_descriptions

        # cleans instance variable for next <item> node
        self.item_descriptions = []
        
        return item_descriptions
    

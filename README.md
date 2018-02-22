# Python's Crawler for AutoEsporte's Magazine News Feed!

* Implemented with python 3.6.1;
* Backend service developed with Django framework;
* Usage of gunicorn server; 
* Dockerized project in a container.

This project consumes an XML file from AutoEsporte's magazine feed which can be acessed at
http://revistaautoesporte.globo.com/rss/ultimas/feed.xml

This crawler service parses all useful information from XML and HTML of the last news of the
magazine and converts it into an organized an easy-to-understand JSON.


# main image 
FROM python:3

# creates directory AND copies all files
ADD . /crawler_app

WORKDIR /crawler_app

# installs all libraries from requirements.txt
RUN pip install -r requirements.txt

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# testing
EXPOSE 5858

# runs shell script to start the server
CMD ["sh", "./start_server.sh"]


# Python's Crawler for AutoEsporte's Magazine News Feed!

## Details

* Implemented with python 3.6.1;
* Backend service developed with Django framework;
* Token-based authentication to use the service;
* Unit tested with unittest library;
* Dockerized project in a container.

This project consumes an XML file from AutoEsporte's magazine feed which can be acessed at
http://revistaautoesporte.globo.com/rss/ultimas/feed.xml

This crawler service parses all useful information from XML and HTML of the last news of the
magazine and converts it into an organized an easy-to-understand JSON.

## Installation

* Build the Dockerfile and run it exposing the port 8000 (required by Django). The shell script 
file **start_server.sh** will be executed to run the server.

## File Summary

* ```/api/views.py```  **-->** contains the **main crawler function** to handle the requests and parse the XML file; <br/>
* ```/api/urls.py```   **-->** endpoints of the service; <br/>
* ```/api/models.py``` **-->** classes used to parse the file and build objects for the JSON output; <br/>
* ```/api/helper_functions/crawler_functions.py``` **-->** functions to manipulate the xml data; <br/>
* ```/api/tests/xml_test.txt``` **-->** simple xml used for testing the xml parser; <br/>
* ```/api/tests/tests.py``` **-->** tests for the crawler views and functions. <br/>

## Api endpoints

```/api/``` : GET root route of the service, sends a welcome JSON to the user; <br/>
```/api/crawler``` : GET route that parses the XML and returns the final JSON. Requires authentication token; <br/>
```/api/get_auth_token``` : POST route that requires a JSON with a username and password to retrieve an auth token. <br/>

## Authentication

A single user was created to demonstrate the authentication of the application. However, if one wanted to expand this 
service, such task would be easy because the addition of new users to the database is already configured to generate 
a new token for that person.

The credentials of the generated user are as follows and are required for the parsing route: ```/api/crawler```:

```
username: globo
password: 123
```

These credentials are required as a JSON body of a POST request to the ```/api/get_auth_token``` route, which returns
the token of the user since GET requests to the service ```/api/crawler``` requires an HTTP header as follows:

```Authentication: Token user_token```

GET to ```/api/crawler``` without the auth token will generate a 401 http status message and a 400 message for wrong 
username or pass.

## Examples

* Response of a GET request to the root route of the api: ```/api/```

```
{
    "Crawler service": "Welcome user! Dont forget to login to use the service."
}
```

* POST JSON body to get an auth token from the authentication route: ```/api/get_auth_token```

```
{
    "username": "globo",
    "password": "123"	
}
```

* Received token from the auth route:

```
{
    "token": "a41feb4cf545ce14de7929131683072b938d018e"
}
```

After receiving the token, one can access the crawler service by supplying the token in the headers of subsequent HTTP requests.

* HTTP Header example of an authenticated request:
```
Authorization: Token a41feb4cf545ce14de7929131683072b938d018e
```

* JSON result of an authenticated GET request to the crawler service: ```/api/crawler```:

```
{
    "feed": [
        {
            "item": {
                "description": [
                    {
                        "content": "https://s2.glbimg.com/xlMjearSH73wx9T0v9L-kI3PAvk=/e.glbimg.com/og/ed/f/original/2018/02/22/phonelifestyle-resize-1024x576.jpg",
                        "type": "image"
                    },
                    {
                        "content": "Se você é tão aventureiro que ter um dos SUVs offroad mais icônicos não basta, a Land Rover agora quer que você tenha um celular aventureiro . O Land Rover Explore é inspirado no Discovery e promete ser muito resistente para encarar quedas, água e altas temperaturas. O aparelho vai ser apresentado nos próximos dias, durante o Congresso Mundial de Mobilidade, em Bercelona, e depois estará exposto no Salão de Genebra, no começo de março. Mas, ainda não existe previsão de vendas do smartphone no Brasil .",
                        "type": "text"
                    },
                    {
                        "content": "O aparelho foi desenvolvido pela Land Rover em parceria com o Bullit Group e conta com sistema operacional Android . A grande diferença do Land Rover Explorer, segundo a empresa, é que o celular suporta condições extremas, como imersão de até 1,8 metro de profundidade na água, altas temperaturas, umidade, choque térmico e exposição à vibração . Ou seja, é o aparelho perfeito para mergulhadores, ciclistas, corredores e todo tipo de atleta, mas também promete ser um aparelho de design “para escritório”.",
                        "type": "text"
                    },
                    {
                        "content": "A tela tem 5 polegadas e resolução Full HD. Outro grande diferencial é a bateria, que promete d uração de 2 dias , acompanhando o dono em sua jornada do início ao fim. Também está disponível o pacote opcional Adventure Pack , que conta com encaixe para bicicletas, bateria extra e GPS mais preciso. Ou seja: dá para começar uma trilha no SUV e terminar a pé, seguindo a rota do celular.",
                        "type": "text"
                    },
                    {
                        "content": "As primeiras unidades do celular serão todas equipadas com esse pacote de opcionais e custarão a bagatela de 649 euros, o equivalente a R$ 2.583 , sem impostos.",
                        "type": "text"
                    },
                    {
                        "content": [
                            "http://revistaautoesporte.globo.com/Noticias/noticia/2016/01/land-rover-defender-deixa-de-ser-produzido-apos-68-anos.html",
                            "http://revistaautoesporte.globo.com/Noticias/noticia/2017/12/novo-land-rover-defender-nao-sera-parecido-com-o-antigo.html",
                            "http://revistaautoesporte.globo.com/Noticias/noticia/2017/09/este-e-o-volante-inteligente-que-jaguar-land-rover-quer-colocar-em-carros-compartilhados.html",
                            "https://revistaautoesporte.globo.com/testes/noticia/2018/02/novo-land-rover-range-rover-velar-teste.html"
                        ],
                        "type": "links"
                    }
                ],
                "link": "https://revistaautoesporte.globo.com/Noticias/noticia/2018/02/land-rover-explorer-celular-defender.html",
                "title": "Land Rover Explorer é o celular aventureiro inspirado no Discovery"
            }
        }, 
        
        (...)
        
        }
    }]
}        
```

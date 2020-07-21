# WATTx Software Engineer Challenge: Top Coins by Shahar Lackritz

## Installation and Running the Server
The script requires Python 3.8 for running properly (although it might work fine on previous versions). 
Also, you can use your preferred possibility of the script installation:

### Manual installation
For running the script properly, except for the already built-in Python libraries, 
the requests library should be installed (2.24 ver or higher). 
This could be achieved by typing:
`pip install requests`

after installing the libraries, you can run the server by opening the terminal in the project's directory at type:
 `python3 main.py`

### Docker
With Docker, you can simply run the terminal inside the 'top_coins_wattx' project and run:
`sudo docker-compose up`
after typing the command above, the server should be up and running.

## Calling the Server
After the server is up and running, one can try and call it. The server should return the top 
ranked crypto-currency and their respective USD price in JSON. The default server IP is your home address (127.0.0.1)
and the default port is 6667. The server also accepts the 'limit' parameter, which determined the number of currencies returned by the server 
(default and maximum set to 200).

An example call:


```
$  curl 127.0.0.1:6667?limit=10

[{'Rank': 1, 'Symbol': 'BTC', 'Price USD': 9189.11496478}, {'Rank': 2, 'Symbol': 'ETH', 'Price USD': 238.522413194}, {'Rank': 3, 'Symbol': 'LINK', 'Price USD': 7.8025887641}, {'Rank': 4, 'Symbol': 'EOS', 'Price USD': 2.59410208229}, {'Rank': 5, 'Symbol': 'XRP', 'Price USD': 0.197818048684}, {'Rank': 6, 'Symbol': 'BCH', 'Price USD': 224.466859379}, {'Rank': 7, 'Symbol': 'SXP', 'Price USD': 1.74517150315}, {'Rank': 8, 'Symbol': 'ETC', 'Price USD': 6.12076090668}, {'Rank': 9, 'Symbol': 'VET', 'Price USD': 0.016571179272}, {'Rank': 10, 'Symbol': 'XLM', 'Price USD': 0.0990541834488}]
```


## Problem and Solution
### The problem:
The problem described in the task was making a prototype price list service for top crypto assets.

### The solution
For resolving the problem, the following steps were taken:
* Opening a WSGI server using the wsgiref built-in Python library. 

Also, every time a client is calling the ever, the following steps are performed:
* Parsing the 'limit' parameter configured by the user with the method 'set_limit'
* Collecting the top ranked coins from the CryptoCompare API service using the 'requests' library by the cryptocompare_request method
* Collecting the USD price of the currencies from CoinMarketCap API services using 'requests' by the coinmarketcap_request method
* Merging the data that was collected from the two API services (merge_data method) and return it to the client

As requested, the program is consist of (at least) 3 independent services:
* coinmarketcap_request - keeps the up-to-date pricing information
* cryptocompare_request -  keeps the up-to-date ranking information
* main - exposes an HTTP endpoint that returns the up-to-date list of 200 top coins prices

## Reasoning Behind Technical Choices
WSGI - Although some other methods might offer more options and flexibility, WSGI was chosen as the inter-service communication
for the following reasons:
* It offers exactly what was required by the task
* It's simple and already has a built-in library
* Using frameworks was not recommended, which makes the implementation of some other methods a much more complex task

The server returns JSON
* As both API services return JSON, merging them into another JSON was less complicated
* you gave me the option to use JSON

Using 'requests' to make API calls
* As far as I know, it's the easiest simplest way to do so.


## Future work
* This program assumes that the clients configure the input correctly. Hence, the input includes only the 'limit'
 parameter in the URL, and just after it an '=' sign and a number (curl 127.0.0.1:6667?limit=200
) for example. The program should also handle incorrect input.

* Authentication tokens are kept in the open for the moment, as I assume you need to use the same tokens as mine. 
In later versions, for security reasons, the tokens must not be uploaded to the git but restored only locally.

* Some of the currencies featured in CryptoCompare API do not appear in CoinMarketCap API 
(about 8% especially from the lower ranks). Further investigation is required.

possible solutions:
* Get prices from another API that features those currencies
* Find another request in CoinMarket that features those currencies

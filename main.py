from wsgiref.simple_server import make_server
import logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class coinList():

    def __init__(self, limit_raw):
        self.ranked_list = []
        self.limit = self.set_limit(limit_raw)

    def set_limit(self, limit_raw):
        # This method parses the 'limit' parameter configured by the client (default value = 200)
        if '=' in limit_raw:
            key, value = limit_raw.split('=')
            if key == 'limit':
                limit = value
            else:
                limit = 200
        else:
            limit = 200
        return limit

    def cryptocompare_request(self, page):
        # This method gets the current ranking information for the top assets from CryptoCompare
        url = 'https://min-api.cryptocompare.com/data/top/totalvolfull'
        parameters = {
            'limit': '100',
            'page': str(page),
            'tsym': 'USD'
        }
        headers = {
            'authorization': '6b52351bf25b131dc09476956e07a14a0452d4a653fe69a6be14c9f0c2863da'
        }
        session = Session()
        session.headers.update(headers)
        logging.info('Collecting data from CryptoCompare')
        try:
            response = session.get(url, params=parameters)
            if response.status_code == 200:
                logging.info('Data from CryptoCompare collected successfully')
            else:
                logging.info('status code: '+ str(response.status_code) +'message: '+ response.text)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logging.info(e)


    def coinmarketcap_request(self):
        # This method gets the current USD prices of the coins from CoinMarketCap
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD',
            'aux': 'cmc_rank'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '9489f4c0-5717-498e-925e-67ada8a8e68d',
        }

        session = Session()
        session.headers.update(headers)
        logging.info('Collecting data from CoinMarketCap')

        try:
            response = session.get(url, params=parameters)
            if response.status_code == 200:
                logging.info('Data from CoinMarketCap collected successfully')
            else:
                logging.info('status code: '+ str(response.status_code) +'message: '+ response.text)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logging.info(e)

    def collect_data(self):
        # Calls the cryptocompare_request and the coinmarketcap_request methods to collect the relevant data
        # As each cryptocompare request gets maximum 100 values, two requests are initiated in case of limit > 100
        self.cryptocompare_data = self.cryptocompare_request(0)['Data']
        if int(self.limit) > 100:
            self.cryptocompare_data = self.cryptocompare_data+self.cryptocompare_request(1)['Data']
        self.coinmarketcap_data = self.coinmarketcap_request()

    def find_price(self, symbol):
        # This method pairs a currency symbol to it's USD price found in the json response from CoinMarketCap
        # If a currency price is not found, the price is set to 0 and a logging message appears
        for coin in self.coinmarketcap_data['data']:
            if symbol == coin['symbol']:
                return coin['quote']['USD']['price']
        logging.info('Price of '+symbol+' was not found')
        return 0

    def merge_data(self):
        # This method merges the relevant data from the two sources.
        # Gets the ranking and the currency symbol from CryptoCompare and the USD price from CoinMarketCap
        # The 'limit' parameter determines the number of currencies merged
        logging.info('Merging data')
        for coin, i in zip(self.cryptocompare_data, range(int(self.limit))):
            coin_dic={}
            coin_dic['Rank'] = i+1
            coin_dic['Symbol'] = coin['CoinInfo']['Name']
            coin_dic['Price USD'] = self.find_price(coin_dic['Symbol'])
            self.ranked_list.append(coin_dic)


def web_app(environment, response):
    # sets a wsgi client-server interaction
    status = '200 OK'
    headers = [('content-type', 'application/json')]
    response(status, headers)
    coinlist = coinList(environment['QUERY_STRING'])
    coinlist.collect_data()
    coinlist.merge_data()
    return [(str(coinlist.ranked_list) + '\n').encode('utf-8')]


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    with make_server('', 6667, web_app) as server:
        print('Serving on port 6667')
        server.serve_forever()


if __name__ == "__main__":
    main()
import os
import json
import tornado.ioloop
import tornado.web
import requests
from dotenv import load_dotenv

from get_ip_address import get_public_ip

# Load environment variables from .env file
load_dotenv()

# Load environment variables
API_KEY = os.getenv("GUARDARIAN_API_KEY")
SECRET_KEY = os.getenv("GUARDARIAN_SECRET_KEY")

if not API_KEY:
    raise ValueError("No API key found. Please set the GUARDARIAN_API_KEY environment variable.")
if not SECRET_KEY:
    raise ValueError("No secret key found. Please set the GUARDARIAN_SECRET_KEY environment variable.")

# Function to handle API requests
def api_request(method, endpoint, params=None, data=None):
    try:
        headers = {
            'x-api-key': API_KEY,
            'x-secret-key': SECRET_KEY,
            'Content-Type': 'application/json'
        }
        url = f'https://api-payments.guardarian.com/v1/{endpoint}'
        print(f'Making {method} request to URL: {url}')
        response = requests.request(method, url, headers=headers, params=params, json=data)
        print(f'Request Headers: {headers}')
        print(f'Request Body: {data}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Tornado Request Handlers

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Guardarian API Integration!")

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        status = api_request('GET', 'status')
        if status:
            self.write(status)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch status'})

class CurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        currencies = api_request('GET', 'currencies')
        if currencies:
            self.write(currencies)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch currencies'})

class CurrencyDetailHandler(tornado.web.RequestHandler):
    def get(self, ticker):
        currency_detail = api_request('GET', f'currencies/{ticker}')
        if currency_detail:
            self.write(currency_detail)
        else:
            self.set_status(500)
            self.write({'error': f'Failed to fetch details for currency {ticker}'})

class FiatCurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        fiat_currencies = api_request('GET', 'currencies/fiat')
        if fiat_currencies:
            self.write({"fiat_currencies": fiat_currencies})  # Wrap list in a dictionary
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch fiat currencies'})

class CryptoCurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        crypto_currencies = api_request('GET', 'currencies/crypto')
        if crypto_currencies:
            self.write({"crypto_currencies": crypto_currencies})  # Wrap list in a dictionary
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch crypto currencies'})

class TransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            customer_ip = self.request.headers.get("X-Real-IP")
            if not customer_ip:
                customer_ip = get_public_ip()
            url = "https://api-payments.guardarian.com/v1/transaction"
            headers = {
                "x-api-key": API_KEY,
                "x-secret-key": SECRET_KEY,
                "Content-Type": "application/json",
                "x-forwarded-for": customer_ip
            }

            # Debugging Output
            print("URL:", url)
            print("Headers:", headers)
            print("Data:", data)

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            transaction = response.json()
            
            self.write({"status": "success", "transaction": transaction})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"status": "error", "message": "Invalid JSON"})
        except requests.RequestException as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

class TransactionDetailHandler(tornado.web.RequestHandler):
    def get(self, transaction_id):
        transaction_detail = api_request('GET', f'transaction/{transaction_id}')
        if transaction_detail:
            self.write(transaction_detail)
        else:
            self.set_status(500)
            self.write({'error': f'Failed to fetch transaction {transaction_id}'})

class TransactionsHandler(tornado.web.RequestHandler):
    def get(self):
        transactions = api_request('GET', 'transactions')
        if transactions:
            self.write(transactions)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch transactions'})

class EstimateHandler(tornado.web.RequestHandler):
    def get(self):
        from_currency = self.get_argument('from_currency')
        to_currency = self.get_argument('to_currency')
        amount = self.get_argument('amount')
        params = {'from_currency': from_currency, 'to_currency': to_currency, 'amount': amount}
        estimate = api_request('GET', 'estimate', params=params)
        if estimate:
            self.write(estimate)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch estimate'})

class EstimateByCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        estimate_by_category = api_request('GET', 'estimate/by-category')
        if estimate_by_category:
            self.write(estimate_by_category)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch estimate by category'})

class MarketInfoHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        market_info = api_request('GET', f'market-info/min-max-range/{from_to}')
        if market_info:
            self.write(market_info)
        else:
            self.set_status(500)
            self.write({'error': f'Failed to fetch market info for {from_to}'})

class SubscriptionHandler(tornado.web.RequestHandler):
    def get(self):
        subscriptions = api_request('GET', 'subscriptions')
        if subscriptions:
            self.write(subscriptions)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch subscriptions'})

class B2BCurrenciesHandler(tornado.web.RequestHandler):
    def get(self):
        b2b_currencies = api_request('GET', 'b2b/currencies')
        if b2b_currencies:
            self.write(b2b_currencies)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch B2B currencies'})

class B2BMinMaxRangeHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        min_max_range = api_request('GET', f'b2b/min-max-range/{from_to}')
        if min_max_range:
            self.write(min_max_range)
        else:
            self.set_status(500)
            self.write({'error': f'Failed to fetch min-max range for {from_to}'})

class AddBankAccountHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            response = api_request('POST', 'b2b/add-bank-account', data=data)
            if response:
                self.set_status(201)
                self.write(response)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to add bank account'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON'})
        except requests.RequestException as e:
            self.set_status(500)
            self.write({'error': str(e)})

class AddCryptoWalletHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            response = api_request('POST', 'b2b/add-crypto-wallet', data=data)
            if response:
                self.set_status(201)
                self.write(response)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to add crypto wallet'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON'})
        except requests.RequestException as e:
            self.set_status(500)
            self.write({'error': str(e)})

class PayoutAddressesHandler(tornado.web.RequestHandler):
    def get(self):
        payout_addresses = api_request('GET', 'b2b/payout-addresses')
        if payout_addresses:
            self.write(payout_addresses)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch payout addresses'})

class B2BEstimateHandler(tornado.web.RequestHandler):
    def get(self):
        from_currency = self.get_argument('from_currency')
        to_currency = self.get_argument('to_currency')
        from_amount = self.get_argument('from_amount')
        from_network = self.get_argument('from_network', None)
        to_network = self.get_argument('to_network', None)
        params = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'from_amount': from_amount,
            'from_network': from_network,
            'to_network': to_network,
        }
        estimate = api_request('GET', 'b2b/estimate', params=params)
        if estimate:
            self.write(estimate)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch estimate'})

class CreateB2BTransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            response = api_request('POST', 'b2b/transaction', data=data)
            if response:
                self.set_status(201)
                self.write(response)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to create B2B transaction'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON'})
        except requests.RequestException as e:
            self.set_status(500)
            self.write({'error': str(e)})

class B2BTransactionsHandler(tornado.web.RequestHandler):
    def get(self):
        params = {
            'offset': self.get_argument('offset', None),
            'limit': self.get_argument('limit', None),
            'from_date': self.get_argument('from_date', None),
            'to_date': self.get_argument('to_date', None),
            'sorting': self.get_argument('sorting', None),
        }
        transactions = api_request('GET', 'b2b/transactions', params=params)
        if transactions:
            self.write(transactions)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch B2B transactions'})

class CountryHandler(tornado.web.RequestHandler):
    def get(self):
        countries = api_request('GET', 'countries')
        if countries:
            self.write(countries)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to fetch countries'})

# KYC Handler
class KYCHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            kyc_data = api_request('POST', 'kyc', data=data)
            if kyc_data:
                self.write({"status": "success", "kyc": kyc_data})
            else:
                self.set_status(500)
                self.write({"status": "error", "message": "Failed to process KYC"})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"status": "error", "message": "Invalid JSON"})
        except requests.RequestException as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

class KYCStatusHandler(tornado.web.RequestHandler):
    def get(self, kyc_id):
        kyc_status = api_request('GET', f'kyc/{kyc_id}')
        if kyc_status:
            self.write(kyc_status)
        else:
            self.set_status(500)
            self.write({'error': f'Failed to fetch KYC status for {kyc_id}'})

# Tornado Application Setup
def make_app():
    return tornado.web.Application([
        (r"/v1/", MainHandler),
        (r"/v1/status", StatusHandler),
        (r"/v1/currencies", CurrencyHandler),
        (r"/v1/currencies/fiat", FiatCurrencyHandler),
        (r"/v1/currencies/crypto", CryptoCurrencyHandler),
        (r"/v1/currencies/([A-Z]+)", CurrencyDetailHandler),
        (r"/v1/transaction", TransactionHandler),
        (r"/v1/transaction/([a-zA-Z0-9-]+)", TransactionDetailHandler),
        (r"/v1/transactions", TransactionsHandler),
        (r"/v1/estimate", EstimateHandler),
        (r"/v1/estimate/by-category", EstimateByCategoryHandler),
        (r"/v1/market-info/min-max-range/([A-Z_]+)", MarketInfoHandler),
        (r"/v1/subscriptions", SubscriptionHandler),
        (r"/v1/countries", CountryHandler),
        (r"/v1/b2b/currencies", B2BCurrenciesHandler),
        (r"/v1/b2b/min-max-range/([A-Z_]+)", B2BMinMaxRangeHandler),
        (r"/v1/b2b/add-bank-account", AddBankAccountHandler),
        (r"/v1/b2b/add-crypto-wallet", AddCryptoWalletHandler),
        (r"/v1/b2b/payout-addresses", PayoutAddressesHandler),
        (r"/v1/b2b/estimate", B2BEstimateHandler),
        (r"/v1/b2b/transaction", CreateB2BTransactionHandler),
        (r"/v1/b2b/transactions", B2BTransactionsHandler),
        (r"/v1/kyc", KYCHandler),
        (r"/v1/kyc/([a-zA-Z0-9-]+)", KYCStatusHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

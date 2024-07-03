import os
import json
import tornado.ioloop
import tornado.web
import requests

# Please ensure access keys are stored in environment variable before running the script
API_KEY = os.getenv("GUARDARIAN_API_KEY")
SECRET_KEY = os.getenv("GUARDARIAN_SECRET_KEY")

if not API_KEY:
    raise ValueError("No API key found. Please set the GUARDARIAN_API_KEY environment variable.")
if not SECRET_KEY:
    raise ValueError("No secret key found. Please set the GUARDARIAN_SECRET_KEY environment variable.")

# Function that will handle API requests
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

# Request Handlers

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Guardarian API Integration!")

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            status = api_request('GET', 'status')
            if status:
                self.write(status)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch status'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class CurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            currencies = api_request('GET', 'currencies')
            if currencies:
                self.write(currencies)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch currencies'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class CurrencyDetailHandler(tornado.web.RequestHandler):
    def get(self, ticker):
        try:
            currency_detail = api_request('GET', f'currencies/{ticker}')
            if currency_detail:
                self.write(currency_detail)
            else:
                self.set_status(500)
                self.write({'error': f'Failed to fetch details for currency {ticker}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class FiatCurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            fiat_currencies = api_request('GET', 'currencies/fiat')
            if fiat_currencies:
                self.write({"fiat_currencies": fiat_currencies})  # Wrap list in a dictionary
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch fiat currencies'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class CryptoCurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            crypto_currencies = api_request('GET', 'currencies/crypto')
            if crypto_currencies:
                self.write({"crypto_currencies": crypto_currencies})  # Wrap list in a dictionary
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch crypto currencies'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

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

            # Debugging
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
        try:
            transaction_detail = api_request('GET', f'transaction/{transaction_id}')
            if transaction_detail:
                self.write(transaction_detail)
            else:
                self.set_status(500)
                self.write({'error': f'Failed to fetch transaction {transaction_id}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class TransactionsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            transactions = api_request('GET', 'transactions')
            if transactions:
                self.write(transactions)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch transactions'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class EstimateHandler(tornado.web.RequestHandler):
    def get(self):
        try:
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
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class EstimateByCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            estimate_by_category = api_request('GET', 'estimate/by-category')
            if estimate_by_category:
                self.write(estimate_by_category)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch estimate by category'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class MarketInfoHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        try:
            market_info = api_request('GET', f'market-info/min-max-range/{from_to}')
            if market_info:
                self.write(market_info)
            else:
                self.set_status(500)
                self.write({'error': f'Failed to fetch market info for {from_to}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class SubscriptionHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            subscriptions = api_request('GET', 'subscriptions')
            if subscriptions:
                self.write(subscriptions)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch subscriptions'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class B2BCurrenciesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            b2b_currencies = api_request('GET', 'b2b/currencies')
            if b2b_currencies:
                self.write(b2b_currencies)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch B2B currencies'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class B2BMinMaxRangeHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        try:
            min_max_range = api_request('GET', f'b2b/min-max-range/{from_to}')
            if min_max_range:
                self.write(min_max_range)
            else:
                self.set_status(500)
                self.write({'error': f'Failed to fetch min-max range for {from_to}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

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
        try:
            payout_addresses = api_request('GET', 'b2b/payout-addresses')
            if payout_addresses:
                self.write(payout_addresses)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch payout addresses'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class B2BEstimateHandler(tornado.web.RequestHandler):
    def get(self):
        try:
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
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

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
        try:
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
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class CountryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            countries = api_request('GET', 'countries')
            if countries:
                self.write(countries)
            else:
                self.set_status(500)
                self.write({'error': 'Failed to fetch countries'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# KYC
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
        try:
            kyc_status = api_request('GET', f'kyc/{kyc_id}')
            if kyc_status:
                self.write(kyc_status)
            else:
                self.set_status(500)
                self.write({'error': f'Failed to fetch KYC status for {kyc_id}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

#  Application Setup
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

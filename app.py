import tornado.ioloop
import tornado.web
import requests
import json

# Define the API base URL
API_BASE_URL = 'https://api-payments.guardarian.com'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Guardarian API")

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        response = requests.get(f"{API_BASE_URL}/v1/status", headers={"accept": "application/json"})
        
        self.set_status(response.status_code)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(response.text)

class CurrencyHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get(f"{API_BASE_URL}/v1/currencies", headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class CurrencyByTickerHandler(tornado.web.RequestHandler):
    def get(self, ticker):
        try:
            response = requests.get(f"{API_BASE_URL}/v1/currencies/{ticker}", headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class FiatCurrenciesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get(f"{API_BASE_URL}/v1/currencies/fiat", headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class CryptoCurrenciesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            response = requests.get(f"{API_BASE_URL}/v1/currencies/crypto", headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class TransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            request_body = json.loads(self.request.body)

            response = requests.post(
                f"{API_BASE_URL}/v1/transaction",
                headers={
                    "accept": "application/json",
                    "x-api-key": "010cb33d-a368-4e4e-bf59-cfbc44ffcb66",
                    "x-forwarded-for": self.request.remote_ip  # Forward customer's IP
                },
                json=request_body
            )

            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class TransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            request_body = json.loads(self.request.body)

            print("Request Body:", request_body)

            response = requests.post(
                f"{API_BASE_URL}/v1/transaction",
                headers={
                    "accept": "application/json",
                    "x-api-key": "010cb33d-a368-4e4e-bf59-cfbc44ffcb66",
                    "x-forwarded-for": self.request.remote_ip  # Forward customer's IP
                },
                json=request_body
            )

            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)

            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            print("Request Exception:", e)

            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class TransactionDetailsHandler(tornado.web.RequestHandler):
    def get(self, id):
        try:
            response = requests.get(f"{API_BASE_URL}/v1/transaction/{id}", headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class TransactionsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            secret_key = self.request.headers.get('010cb33d-a368-4e4e-bf59-cfbc44ffcb66')

            if not secret_key:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid secret key"}))
                return

            offset = self.get_argument('offset', default=0)
            limit = self.get_argument('limit', default=50)
            from_date = self.get_argument('from_date', default=None)
            to_date = self.get_argument('to_date', default=None)
            sorting = self.get_argument('sorting', default='desc')
            updated_from_date = self.get_argument('updated_from_date', default=None)
            updated_to_date = self.get_argument('updated_to_date', default=None)

            url = f"{API_BASE_URL}/v1/transactions?offset={offset}&limit={limit}&sorting={sorting}"
            if from_date:
                url += f"&from_date={from_date}"
            if to_date:
                url += f"&to_date={to_date}"
            if updated_from_date:
                url += f"&updated_from_date={updated_from_date}"
            if updated_to_date:
                url += f"&updated_to_date={updated_to_date}"

            response = requests.get(url, headers={"x-secret-key": secret_key, "accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class EstimateHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            from_currency = self.get_argument('from_currency')
            from_network = self.get_argument('from_network', default=None)
            from_amount = self.get_argument('from_amount', default=None)
            to_amount = self.get_argument('to_amount', default=None)
            to_currency = self.get_argument('to_currency')
            to_network = self.get_argument('to_network', default=None)
            deposit_type = self.get_argument('deposit_type', default=None)
            deposit_category = self.get_argument('deposit_category', default=None)
            payout_type = self.get_argument('payout_type', default=None)
            estimate_type = self.get_argument('type', default=None)
            fees_included = self.get_argument('fees_included', default='true')
            customer_country = self.get_argument('customer_country', default=None)

            url = f"{API_BASE_URL}/v1/estimate?from_currency={from_currency}&to_currency={to_currency}"
            if from_network:
                url += f"&from_network={from_network}"
            if from_amount:
                url += f"&from_amount={from_amount}"
            if to_amount:
                url += f"&to_amount={to_amount}"
            if to_network:
                url += f"&to_network={to_network}"
            if deposit_type:
                url += f"&deposit_type={deposit_type}"
            if deposit_category:
                url += f"&deposit_category={deposit_category}"
            if payout_type:
                url += f"&payout_type={payout_type}"
            if estimate_type:
                url += f"&type={estimate_type}"
            if fees_included:
                url += f"&fees_included={fees_included}"
            if customer_country:
                url += f"&customer_country={customer_country}"

            response = requests.get(url, headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class EstimateByCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            from_currency = self.get_argument('from_currency')
            from_network = self.get_argument('from_network', default=None)
            from_amount = self.get_argument('from_amount', default=None)
            to_currency = self.get_argument('to_currency')
            to_network = self.get_argument('to_network', default=None)
            payment_category = self.get_argument('payment_category')
            payout_type = self.get_argument('payout_type', default=None)
            fees_included = self.get_argument('fees_included', default='true')

            url = f"{API_BASE_URL}/v1/estimate/by-category?from_currency={from_currency}&to_currency={to_currency}&payment_category={payment_category}"
            if from_network:
                url += f"&from_network={from_network}"
            if from_amount:
                url += f"&from_amount={from_amount}"
            if to_network:
                url += f"&to_network={to_network}"
            if payout_type:
                url += f"&payout_type={payout_type}"
            if fees_included:
                url += f"&fees_included={fees_included}"

            response = requests.get(url, headers={"accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class MarketInfoMinMaxRangeHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        try:
            url = f"{API_BASE_URL}/v1/market-info/min-max-range/{from_to}"
            response = requests.get(url, headers={"accept": "application/json"})            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class SubscriptionsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/subscriptions"

            response = requests.get(url, headers={"x-api-key": "YOUR_PARTNER_API_KEY"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class SubscriptionByIdHandler(tornado.web.RequestHandler):
    def get(self, subscription_id):
        try:
            url = f"{API_BASE_URL}/v1/subscription/{subscription_id}"

            response = requests.get(url, headers={"x-api-key": "YOUR_PARTNER_API_KEY"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class B2BCurrenciesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/currencies"
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class B2BMinMaxRangeHandler(tornado.web.RequestHandler):
    def get(self, from_to):
        try:
            url = f"{API_BASE_URL}/v1/b2b/min-max-range/{from_to}"
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

class AddBankAccountHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/add-bank-account"
            x_api_key = self.request.headers.get("x-api-key")
            body = json.loads(self.request.body.decode('utf-8'))

            # Make a POST request to the Guardarian
            response = requests.post(url, json=body, headers={"x-api-key": x_api_key, "accept": "application/json"})
            
            response.raise_for_status()

            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return an appropriate error response
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            elif response.status_code == 403:
                self.set_status(403)
                self.write(json.dumps({"error": "Forbidden request error"}))
            elif response.status_code == 404:
                self.set_status(404)
                self.write(json.dumps({"error": "Not found"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class AddCryptoWalletHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/add-crypto-wallet"
            x_api_key = self.request.headers.get("x-api-key")
            body = json.loads(self.request.body.decode('utf-8'))

            # Make a POST request to the Guardarian 
            response = requests.post(url, json=body, headers={"x-api-key": x_api_key, "accept": "application/json"})
            
            response.raise_for_status()
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return an appropriate error response
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            elif response.status_code == 403:
                self.set_status(403)
                self.write(json.dumps({"error": "Forbidden request error"}))
            elif response.status_code == 404:
                self.set_status(404)
                self.write(json.dumps({"error": "Not found"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class PayoutAddressesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/payout-addresses"
            x_api_key = self.request.headers.get("x-api-key")
            response = requests.get(url, headers={"x-api-key": x_api_key, "accept": "application/json"})
            response.raise_for_status()

            # Forward the status code and response body from the Guardarian API
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return an appropriate error response
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class EstimateExchangeHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/estimate"

            from_currency = self.get_query_argument("from_currency")
            from_network = self.get_query_argument("from_network", default=None)
            from_amount = self.get_query_argument("from_amount")
            to_currency = self.get_query_argument("to_currency")
            to_network = self.get_query_argument("to_network", default=None)

            x_api_key = self.request.headers.get("x-api-key")

            # Prepare query parameters
            params = {
                "from_currency": from_currency,
                "from_network": from_network,
                "from_amount": from_amount,
                "to_currency": to_currency,
                "to_network": to_network
            }

            response = requests.get(url, params=params, headers={"x-api-key": x_api_key, "accept": "application/json"})

            response.raise_for_status()
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return an appropriate error response
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class B2BTransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/transaction"
            x_api_key = self.request.headers.get("x-api-key")
            transaction_data = json.loads(self.request.body)
            response = requests.post(url, json=transaction_data, headers={"x-api-key": x_api_key, "accept": "application/json"})
            response.raise_for_status()
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class B2BTransactionsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/b2b/transactions"
            x_api_key = self.request.headers.get("x-api-key")
            offset = self.get_argument("offset", default=None)
            limit = self.get_argument("limit", default=None)
            from_date = self.get_argument("from_date", default=None)
            to_date = self.get_argument("to_date", default=None)
            sorting = self.get_argument("sorting", default=None)

            params = {
                "offset": offset,
                "limit": limit,
                "from_date": from_date,
                "to_date": to_date,
                "sorting": sorting
            }
            response = requests.get(url, params=params, headers={"x-api-key": x_api_key, "accept": "application/json"})
            response.raise_for_status()
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                self.set_status(401)
                self.write(json.dumps({"error": "Invalid token"}))
            else:
                self.set_status(500)
                self.write(json.dumps({"error": "Internal error"}))

class CountriesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            url = f"{API_BASE_URL}/v1/countries"
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()
            self.set_status(response.status_code)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(response.text)

        except requests.exceptions.RequestException as e:
            # If there's an error with the request to Guardarian API, return a 500 error
            self.set_status(500)
            self.write(json.dumps({"error": "Internal error"}))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),  # Handler for root URL
        (r"/v1/status", StatusHandler),
        (r"/v1/currencies", CurrencyHandler),
        (r"/v1/currencies/([^/]+)", CurrencyByTickerHandler),
        (r"/v1/currencies/fiat", FiatCurrenciesHandler),
        (r"/v1/currencies/crypto", CryptoCurrenciesHandler),
        (r"/v1/transaction", TransactionHandler),
        (r"/v1/transaction/([^/]+)", TransactionDetailsHandler),
        (r"/v1/transactions", TransactionsHandler),
        (r"/v1/estimate", EstimateHandler),
        (r"/v1/estimate/by-category", EstimateByCategoryHandler),
        (r"/v1/market-info/min-max-range/([^/]+)", MarketInfoMinMaxRangeHandler),
        (r"/v1/subscriptions", SubscriptionsHandler),
        (r"/v1/subscription/(\d+)", SubscriptionByIdHandler),
        (r"/v1/b2b/currencies", B2BCurrenciesHandler),
        (r"/v1/b2b/min-max-range/([^/]+)", B2BMinMaxRangeHandler),
        (r"/v1/b2b/add-bank-account", AddBankAccountHandler),
        (r"/v1/b2b/add-crypto-wallet", AddCryptoWalletHandler),
        (r"/v1/b2b/payout-addresses", PayoutAddressesHandler),
        (r"/v1/b2b/estimate", EstimateExchangeHandler),
        (r"/v1/b2b/transaction", B2BTransactionHandler),
        (r"/v1/b2b/transactions", B2BTransactionsHandler),
        (r"/v1/countries", CountriesHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

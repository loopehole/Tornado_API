import os
import json
import tornado.ioloop
import tornado.web
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
API_KEY = os.getenv("GUARDARIAN_API_KEY")
SECRET_KEY = os.getenv("GUARDARIAN_SECRET_KEY")

if not API_KEY:
    raise ValueError("No API key found. Please set the GUARDARIAN_API_KEY environment variable.")
if not SECRET_KEY:
    raise ValueError("No secret key found. Please set the GUARDARIAN_SECRET_KEY environment variable.")

class TransactionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            customer_ip = self.request.headers.get("X-Real-IP")
            if not customer_ip:
                customer_ip = 'your_fallback_ip'  # Replace with a default IP if necessary
            
            url = "https://api-payments.guardarian.com/v1/transaction"
            headers = {
                "x-api-key": API_KEY,
                "x-secret-key": SECRET_KEY,
                "Content-Type": "application/json",
                "x-forwarded-for": customer_ip
            }

            print("URL:", url)
            print("Headers:", headers)
            print("Data:", json.dumps(data, indent=4))

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            transaction = response.json()
            
            self.write({"status": "success", "transaction": transaction})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"status": "error", "message": "Invalid JSON"})
        except requests.RequestException as e:
            print(f'Error: {e.response.text}')  # Print the full response text for debugging
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

def make_app():
    return tornado.web.Application([
        (r"/v1/transaction", TransactionHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

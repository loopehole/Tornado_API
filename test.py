import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_info = response.json()
        return ip_info["ip"]
    except requests.RequestException as e:
        print("Error fetching IP address:", e)
        return None

API_KEY = "010cb33d-a368-4e4e-bf59-cfbc44ffcb66"
SECRET_KEY = "2e24f2d9-0b87-44b6-baba-3247f79cddf3"
customer_ip = get_public_ip()
if not customer_ip:
    raise Exception("Could not fetch public IP address")

url = "https://api-payments.guardarian.com/v1/transaction"
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "x-secret-key": SECRET_KEY,
    "x-forwarded-for": customer_ip
}
data = {
    "from_amount": 1200.24,
    "from_currency": "EUR",
    "to_currency": "BTC",
    "from_network": None,
    "to_network": "BNB",
    "kyc_shared_token": "_act-460a698b-d2bc-4cbc-9456-5f36fee38083",
    "kyc_shared_token_provider": "sumsub",
    "redirects": {
        "successful": "https://guardarian.com/finished/$$",
        "cancelled": "https://guardarian.com/cancelled",
        "failed": "https://guardarian.com/failed"
    },
    "payout_info": {
        "payout_address": "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
        "extra_id": "78239832980",
        "skip_choose_payout_address": False
    },
    "customer": {
        "contact_info": {
            "email": "email@email.com",
            "phone_number": "+3723800037"
        },
        "billing_info": {
            "country_alpha_2": "DE", 
            "us_region_alpha_2": None,
            "region": "Bavaria",
            "city": "Munich",
            "street_address": "Some Street",
            "apt_number": "123",
            "post_index": "80331",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birthday": "01.01.1991",
            "gender": "M"
        }
    },
    "deposit": {
        "payment_category": "VISA_MC",
        "skip_choose_payment_category": False
    },
    "customer_country": "JP", 
    "external_partner_link_id": "3245324"
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("Success:", response.json())
except requests.RequestException as e:
    if response.status_code == 403:
        print("Error: Forbidden. Ensure your API key is valid and has the necessary permissions.")
    else:
        print("Error:", e)
        if response.content:
            print("Response content:", response.content.decode())

    # Print for debugging
    print("Request URL:", url)
    print("Request Headers:", headers)
    print("Request Body:", data)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

import requests

# Get your public IP address
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_info = response.json()
        ip_address = ip_info["ip"]
        print("Public IP Address:", ip_address)  # Print the IP address
        return ip_address
    except requests.RequestException as e:
        print("Error fetching IP address:", e)
        return None

if __name__ == "__main__":
    get_public_ip()

import requests

def hello(name):
    return f"Hello, {name}!"

def paymentLink(key, secret, payload):
    url = "https://tycheextdev.ezbillpay.in/paymentLink"
    headers = {
        "API-Key": key,
        "API-Secret": secret,
        "Content-Type": "application/json"
    }
    payload = payload
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
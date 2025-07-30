import requests
from typing import Tuple, Dict, Any


def hello(name):
    return f"Hello, {name}!"

stagging_url = "https://tycheextdev.ezbillpay.in"
production_url = "https://tycheextprod.ezbillpay.in"

def ping_api(production=False) -> tuple:
    """
    Pings the Tyche API to check connectivity.

    Returns:
        Tuple[dict, int]: JSON response (if any) and HTTP status code.
    """
    url = f'{stagging_url}/ping'
    if production:
        url = f'{production_url}/ping'

    try:
        response = requests.get(url)
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None
    

def paymentLink(key, secret, payload, production=False):
    url = f"{stagging_url}/paymentLink"
    if production:
        url = f"{production_url}/paymentLink"
    headers = {
        "API-Key": key,
        "API-Secret": secret,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        # response.raise_for_status()  # raises HTTPError for bad responses
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None
    
def create_order(key, secret, payload, production=False):
    url = f"{stagging_url}/order"
    if production:
        url = f"{production_url}/paymentLink"
    headers = {
        'API-Key': key,
        'API-Secret': secret,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url,  headers=headers, json=payload)
        # response.raise_for_status()  # raises HTTPError for bad responses
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None

def checkout_order(key :str , secret : str, order_reference : str,  payload : dict[str, str] , production : bool = False) -> tuple[dict, int]:
    
    """
    Submits checkout order to the API.

    Parameters:
        key (str): API key.
        secret (str): API secret key.
        order_reference (str): Reference ID from create_order(), e.g., "ncbW6OJEGDb_SH_Pp07GPw==".
        payload (Dict[str, str]): Payload for checkout.
        production (bool, optional): Use production URL if True. Defaults to False.

    Returns:
        Tuple[Dict, int]: API response and status code.
    """

    url = f"{stagging_url}/check-out"
    if production:
        url = f"{production_url}/paymentLink"
    headers = {
        'API-Key': key,
        'API-Secret': secret,
        'Content-Type': 'application/json'
    }
    payload.update({
        "orderReference": order_reference
    })
    try:
        response = requests.post(url, headers=headers, json=payload)

        # Return JSON response and status code
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        # Handle any exception that might occur during the request
        return str(e), None
    


def get_receipt(key: str, secret: str, reference: str, success: bool = True, production: bool = False) -> Tuple[Dict[str, Any], int]:
    """
    Sends a request to the Tyche /receipt API to fetch payment receipt details.

    Parameters:
        key (str): API key.
        secret (str): API secret.
        reference (str): Reference ID of the order.
        success (bool): Indicates if the transaction was successful. Defaults to True.
        production (bool): Use production URL if True, else staging.

    Returns:
        Tuple[dict, int]: JSON response and HTTP status code.
    """
    url = f'{stagging_url}/receipt'
    if production:
        url = f'{production_url}/receipt'

    headers = {
        'API-Key': key,
        'API-Secret': secret,
        'Content-Type': 'application/json'
    }

    payload = {
        "reference": reference,
        "success": str(success).lower()  # API expects "true"/"false" as strings
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None

def request_refund(
    key: str,
    secret: str,
    payment_id: str,
    request_id: str,
    amount: str,
    production: bool = False
) -> Tuple[Dict[str, Any], int]:
    """
    Sends a refund request to the Tyche /refund API.

    Parameters:
        key (str): API key.
        secret (str): API secret.
        payment_id (str): The ID of the original payment to be refunded.
        request_id (str): Unique identifier for the refund request.
        amount (str): Refund amount (as a string).
        production (bool): If True, use the production URL. Defaults to False.

    Returns:
        Tuple[dict, int]: JSON response and HTTP status code.
    """
    url = f'{stagging_url}/refund'
    if production:
        url = f'{production_url}/refund'

    headers = {
        'API-Key': key,
        'API-Secret': secret,
        'Content-Type': 'application/json'
    }

    payload = {
        "paymentId": payment_id,
        "requestId": request_id,
        "amount": amount
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None

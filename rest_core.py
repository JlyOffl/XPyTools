import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(method, url, headers=None, data=None, timeout=180, retries=3, backoff_factor=0.3):
    """
    Make an HTTP request with retries and error handling.

    :param method: str, HTTP method (GET, POST, etc.)
    :param url: str, the URL to request
    :param headers: dict, HTTP headers
    :param data: dict, request payload
    :param timeout: int, request timeout in seconds
    :param retries: int, number of retries for transient errors
    :param backoff_factor: float, factor for the backoff strategy
    :return: Response object or None if an error occurred
    """
    try:
        # Define a retry strategy
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"],
            backoff_factor=backoff_factor
        )
        
        # Define a retry strategy
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"],
        )

        # Create a session
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        # Make the request
        response = session.request(method, url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()  # Raise an error for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        #logger.error(f"Request Error: {e}")
        return None
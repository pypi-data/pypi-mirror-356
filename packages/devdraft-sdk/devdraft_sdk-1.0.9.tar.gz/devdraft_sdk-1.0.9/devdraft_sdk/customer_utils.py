import json
from devdraft_sdk.api.customers_api import CustomersApi

def list_customers(api_client, **kwargs):
    """
    List all customers using the CustomersApi, returning parsed JSON data.
    Args:
        api_client: An instance of devdraft_sdk.ApiClient configured with auth and host.
        **kwargs: Optional query parameters (e.g., name, email, status, take, skip)
    Returns:
        List of customers as Python dicts, or an empty list if none found.
    Raises:
        Exception if the API call fails.
    """
    customers_api = CustomersApi(api_client)
    response, status, headers = customers_api.customer_controller_find_all_with_http_info(_preload_content=False, **kwargs)
    raw = response.read() if hasattr(response, 'read') else response
    return json.loads(raw.decode('utf-8')) if raw else []

def create_customer(api_client, customer_data):
    """
    Create a new customer using the CustomersApi, returning parsed JSON data.
    Args:
        api_client: An instance of devdraft_sdk.ApiClient configured with auth and host.
        customer_data: An instance of CreateCustomerDto.
    Returns:
        The created customer as a Python dict, or None if not returned.
    Raises:
        Exception if the API call fails.
    """
    customers_api = CustomersApi(api_client)
    response, status, headers = customers_api.customer_controller_create_with_http_info(customer_data, _preload_content=False)
    raw = response.read() if hasattr(response, 'read') else response
    return json.loads(raw.decode('utf-8')) if raw else None

def get_customer(api_client, customer_id):
    """
    Get a customer by ID using the CustomersApi, returning parsed JSON data.
    Args:
        api_client: An instance of devdraft_sdk.ApiClient configured with auth and host.
        customer_id: The ID of the customer to retrieve.
    Returns:
        The customer as a Python dict, or None if not found.
    Raises:
        Exception if the API call fails.
    """
    customers_api = CustomersApi(api_client)
    response, status, headers = customers_api.customer_controller_find_one_with_http_info(customer_id, _preload_content=False)
    raw = response.read() if hasattr(response, 'read') else response
    return json.loads(raw.decode('utf-8')) if raw else None

def update_customer(api_client, customer_id, update_data):
    """
    Update a customer by ID using the CustomersApi, returning parsed JSON data.
    Args:
        api_client: An instance of devdraft_sdk.ApiClient configured with auth and host.
        customer_id: The ID of the customer to update.
        update_data: An instance of UpdateCustomerDto with updated fields.
    Returns:
        The updated customer as a Python dict, or None if not returned.
    Raises:
        Exception if the API call fails.
    """
    customers_api = CustomersApi(api_client)
    response, status, headers = customers_api.customer_controller_update_with_http_info(update_data, customer_id, _preload_content=False)
    raw = response.read() if hasattr(response, 'read') else response
    return json.loads(raw.decode('utf-8')) if raw else None 
import json

def call_and_parse(api_method, *args, **kwargs):
    """
    Universal wrapper for any *_with_http_info endpoint.
    Calls the endpoint, parses the raw response, and returns the data as Python objects.
    Args:
        api_method: The *_with_http_info method to call.
        *args, **kwargs: Arguments to pass to the method.
    Returns:
        Parsed JSON data (dict or list), or None if no data.
    """
    kwargs['_preload_content'] = False
    response, status, headers = api_method(*args, **kwargs)
    raw = response.read() if hasattr(response, 'read') else response
    return json.loads(raw.decode('utf-8')) if raw else None 
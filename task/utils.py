def cors_allowed_origins_func(request_origin, *_):
    # Add your logic to determine if the request origin is allowed
    if request_origin.startswith("http://127.0.0.1:3000"):
        return True
    return False

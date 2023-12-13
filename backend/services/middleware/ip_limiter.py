from flask import request, abort
from functools import wraps

def limit_ip_access(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Replace with the IP addresses you want to allow
        allowed_ips = ['127.0.0.1', '192.168.0.1']

        if request.remote_addr not in allowed_ips:
            abort(403)  # Forbidden

        return func(*args, **kwargs)

    return decorated_function

# If this doesn't work, use INTERNAL_API_TOKEN instead. Generate random token
# at the start, then use it for internal calls and if it doesn't match, abort.
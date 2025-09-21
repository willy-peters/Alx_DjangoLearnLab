# bookshelf/middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Adds a Content-Security-Policy header to responses.
    Adjust directives below to match the external domains you actually use.
    Keep it restrictive during testing; loosen only when necessary.
    """

    def process_response(self, request, response):
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "  # prefer removing 'unsafe-inline' and using nonces/hashes
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
        response["Content-Security-Policy"] = csp
        return response

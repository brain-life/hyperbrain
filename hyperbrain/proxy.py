# https://gist.github.com/anjackson/2888380
import bottle
from wsgiproxy.app import WSGIProxyApp

# Remove "hop-by-hop" headers (as defined by RFC2613, Section 13)
# since they are not allowed by the WSGI standard.
FILTER_HEADERS = [
    'Connection',
    'Keep-Alive',
    'Proxy-Authenticate',
    'Proxy-Authorization',
    'TE',
    'Trailers',
    'Transfer-Encoding',
    'Upgrade',
    ]

def create_proxy(host):
    proxy_app = WSGIProxyApp(host)

    def wrap_start_response(start_response):
        def wrapped_start_response(status, headers_out):
            # Remove "hop-by-hop" headers
            headers_out = [(k,v) for (k,v) in headers_out
                           if k not in FILTER_HEADERS]
            return start_response(status, headers_out)
        return wrapped_start_response
    
    
    def wrapped_proxy_app(environ, start_response):
        start_response = wrap_start_response(start_response)
        return proxy_app(environ, start_response)

    return wrapped_proxy_app



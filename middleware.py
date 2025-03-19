from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from urllib.parse import unquote
import time

class FacebookTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Only for GET requests
        if request.method != 'GET':
            return self.get_response(request)

        if not request.session.session_key:
            # Force Django to create a session
            request.session['temp'] = True
            request.session.save()

        # Get the response
        response = self.get_response(request)

        # Capture fbclid from URL
        fbclid = request.GET.get('fbclid')

        # No _fbc? Create it
        if fbclid and '_fbc' not in request.COOKIES:
            _fbc = f"fb.1.{int(time.time() * 1000)}.{unquote(fbclid)}"
            print(_fbc)
            response.set_cookie(
                '_fbc',
                _fbc,
                max_age=7776000,  # 60 days (in seconds)
                httponly=True,
                samesite='Lax'
            )

        # No _fbp? Create it
        if fbclid and '_fbp' not in request.COOKIES:
            session_key = request.session.session_key or 'unknown'
            _fbp = f"fb.1.{int(time.time() * 1000)}.{urlsafe_base64_encode(force_bytes(session_key))}"
            print(_fbp)
            response.set_cookie(
                '_fbp',
                _fbp,
                max_age=7776000,  # 60 days (in seconds)
                httponly=True,
                samesite='Lax'
            )

        return response

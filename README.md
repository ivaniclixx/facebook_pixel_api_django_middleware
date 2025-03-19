# facebook_pixel_api_django_middleware
A middleware that generates the _fbc and _fbp COOKIES from fbclid, when missing.


Add this file to your project app:

myapp/middleware.py

and configure it in django settings:

MIDDLEWARE = [

'django.contrib.sessions',

'myapp.middleware.FacebookTrackingMiddleware',

]

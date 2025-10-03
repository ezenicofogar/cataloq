import time

class DelayMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add a 300ms delay
        time.sleep(0.9)
        response = self.get_response(request)
        return response

from django.http import HttpRequest

class HtmxMiddleware:
    """
    ### HtmxMiddleware

    This middleware adds the `htmx` headers to each request object under `htmx`.

    - Boosted:               HX-Boosted
    - CurrentURL:            HX-Current-URL
    - HistoryRestoreRequest: HX-History-Restore-Request
    - Prompt:                HX-Prompt
    - Request:               HX-Request
    - Target:                HX-Target
    - TriggerName:           HX-Trigger-Name
    - Trigger:               HX-Trigger
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.htmx = {
            'boosted':               request.headers.get('HX-Boosted'),
            'currentURL':            request.headers.get('HX-Current-URL'),
            'historyRestoreRequest': request.headers.get('HX-History-Restore-Request'),
            'prompt':                request.headers.get('HX-Prompt'),
            'request':               request.headers.get('HX-Request'),
            'target':                request.headers.get('HX-Target'),
            'triggerName':           request.headers.get('HX-Trigger-Name'),
            'trigger':               request.headers.get('HX-Trigger'),
        }
        return self.get_response(request)
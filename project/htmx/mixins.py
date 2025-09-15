from django.http import Http404

class HtmxOr404Mixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.check_condition(request, *args, **kwargs):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def check_condition(self, request, *args, **kwargs):
        return request.htmx.get('request') is not None
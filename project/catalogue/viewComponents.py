from django.views import View, generic

class ComponentHeaderView(generic.TemplateView):
    template_name = 'components/header.html'

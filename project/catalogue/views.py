from django.views import View, generic
from . import models

class IndexView(generic.TemplateView):
    template_name = 'page/index.html'

class CollectionListView(generic.ListView):
    template_name = 'page/collection-list.html'
    queryset = models.Collection.objects.all()
    extra_context = {'title': 'colecciones'}

class CategoryListView(generic.ListView):
    template_name = 'page/category-list.html'
    queryset = models.Category.objects.filter(parent=None)
    extra_context = {'title': 'categorías'}

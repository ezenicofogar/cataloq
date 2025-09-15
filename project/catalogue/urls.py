from django.urls import path
from . import views, viewComponents as comps

urlpatterns = [
    # pages
    path('', views.IndexView.as_view(), name='index'),

    # components
    path('components/header/', comps.ComponentHeaderView.as_view(), name='component-header'),
]

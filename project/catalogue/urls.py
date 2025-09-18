from django.urls import path
from . import views, viewComponents as comps

urlpatterns = [
    # pages
    path('', views.IndexView.as_view(), name='index'),
    path('collection/', views.CollectionListView.as_view(), name='collection-list'), # collection list
    path('category/', views.CategoryListView.as_view(), name='category-list'), # category lsit
    # path('product/'), # product list with filters
    # path('product/detail/<slug:slug>/'), # product detail
    # path('brand/'), # brand list

    # components
    path('components/header/', comps.ComponentHeaderView.as_view(), name='component-header'),
]

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.APIRoot.as_view(), name='api-root'),
    url(r'^product/$', views.Products.as_view(), name='products'),
    url(r'^product/(?P<id>[\d-]+)$', views.ProductItem.as_view(), name='product-item'),
    url(r'^shelf/$', views.Shelfs.as_view(), name='shelfs'),
    url(r'^shelf/prepare/$', views.Prepare.as_view(), name='shelfs-prepare'),
    url(r'^shelf/(?P<id>[\d-]+)$', views.ShelfItem.as_view(), name='shelf-item'),
    url(r'^transport/$', views.Transports.as_view(), name='transports'),
    url(r'^transport/(?P<id>[\d-]+)$', views.TransportItem.as_view(), name='transport-item'),
]

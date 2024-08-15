from django.urls import path
from .views import ProductCreateView, ProductStockUpdateView, OrderCreateView

urlpatterns = [
    path('products', ProductCreateView.as_view(), name='product-create'),
    path('inventories/product/<int:product_id>', ProductStockUpdateView.as_view(), name='product-stock-update'),
    path('orders', OrderCreateView.as_view(), name='order-create'),
]
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Order, OrderItem

class ProductCreateViewTest(APITestCase):

    def test_create_product_success(self):
        url = reverse('product-create')
        data = {
            "sku": "TEST123",
            "name": "Test Product"
        }
        response = self.client.post(url, data, format='json')
        
        # Verificamos que la respuesta sea 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificamos que el producto haya sido creado
        product = Product.objects.get(sku="TEST123")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.stock, 100)

    def test_create_product_missing_fields(self):
        url = reverse('product-create')

        # Quitamos el campo 'name'
        data = {
            "sku": "TEST123"
        }
        response = self.client.post(url, data, format='json')
        
        # Verificamos que la respuesta sea 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_duplicate_sku(self):
        # Creamos un producto inicial
        Product.objects.create(sku="TEST123", name="Initial Product")
        
        url = reverse('product-create')
        data = {
            "sku": "TEST123",
            "name": "Another Product"
        }
        response = self.client.post(url, data, format='json')
        
        # Verificamos que la respuesta sea 400 por un a SKU duplicado
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductStockUpdateViewTest(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(sku="TEST123", name="Test Product", stock=100)

    def test_add_stock_success(self):
        url = reverse('product-stock-update', args=[self.product.id])
        data = {"stock": 50}
        response = self.client.patch(url, data, format='json')
        
        # Verificamos que la respuesta sea 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificamos que el stock haya sido actualizado correctamente
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 150)  # 100 + 50 = 150

    def test_add_stock_negative_value(self):
        url = reverse('product-stock-update', args=[self.product.id])
        data = {"stock": -20}
        response = self.client.patch(url, data, format='json')
        
        # Verificamos que la respuesta sea 200 OK, aunque no es común usar valores negativos para stock
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el stock haya sido reducido
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 80)  # 100 - 20 = 80

    def test_add_stock_product_not_found(self):
        url = reverse('product-stock-update', args=[999])  # ID que no existe
        data = {"stock": 50}
        response = self.client.patch(url, data, format='json')
        
        # Verificar que la respuesta sea 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

class OrderCreateViewTest(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(sku="SKU123", name="Product 1", stock=10, price=15.00)
        self.product2 = Product.objects.create(sku="SKU124", name="Product 2", stock=5, price=30.00)

    def test_create_order_success(self):
        url = reverse('order-create')
        data = {
            "items": [
                {"product": self.product1.id, "quantity": 2, "price": 15.00},
                {"product": self.product2.id, "quantity": 1, "price": 30.00}
            ]
        }
        response = self.client.post(url, data, format='json')
        
        # Verificar que la respuesta sea 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el pedido haya sido creado
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)
        
        # Verificar que el stock haya sido actualizado
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 8)
        self.assertEqual(self.product2.stock, 4)

    def test_create_order_insufficient_stock(self):
        url = reverse('order-create')
        data = {
            "items": [
                {"product": self.product1.id, "quantity": 20, "price": 15.00}
            ]
        }
        response = self.client.post(url, data, format='json')
        
        # Verificamos que la respuesta sea 400 debido a stock insuficiente
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificamos que el pedido no haya sido creado
        self.assertEqual(Order.objects.count(), 0)
import logging
from rest_framework import serializers
from .models import Product, Order, OrderItem

logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('sku','name','stock','created_at')
        read_only_fields = ('stock','created_at')

class ProductStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items','total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        total_price = 0
        for item_data in items_data:
            product = item_data['product']
            if product.stock < item_data['quantity']:
                raise serializers.ValidationError(f"Stock insuficiente para el producto {product.name}")
            if product.stock <= 10:
                print("Stock menor a 10")
                logger.warning(f"Alerta: El producto '{product.name}' tiene un stock bajo ({product.stock} unidades restantes).")
            item = OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=item_data['price'])
            product.stock -= item_data['quantity']
            product.save()

            total_price += item.price * item.quantity

        order.total_price = total_price
        order.save()
        return order
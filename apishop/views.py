from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import get_object_or_404
from .serializers import ProductStockUpdateSerializer, OrderSerializer

class ProductCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductStockUpdateView(APIView):

    def patch(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductStockUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product.stock += serializer.validated_data.get('stock', 0)
            product.save()
            return Response({'message': 'Stock actualizado correctamente', 'stock': product.stock}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        print(request.data)
        
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
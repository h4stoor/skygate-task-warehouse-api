from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import Product, ShelfBox, Shelf, Transport


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Product.objects.all())])
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'quantity')

    def create(self, data):
        quantity = data.get('quantity') or 0
        product = Product.objects.create(name=data['name'], quantity=quantity)
        return product


class ShelfBoxSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    
    class Meta:
        model = ShelfBox
        fields = ('id', 'product', 'quantity')


class ShelfSerializer(serializers.ModelSerializer):
    box1 = ShelfBoxSerializer()
    box2 = ShelfBoxSerializer()
    box3 = ShelfBoxSerializer()
    
    class Meta:
        model = Shelf
        fields = ('id', 'box1', 'box2', 'box3')


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ('id', 'product_request', 'cargo', 'status')

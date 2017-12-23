from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.reverse import reverse

from .models import Product, ShelfBox, Shelf, Transport
from .api.serializers import ProductSerializer, ShelfSerializer, TransportSerializer
from .const import *


class Responses:
    def response_200(self, data, label=False, success=True):
        response = dict()
        
        if label:
            response[self.label] = data
        else:
            response = data
            
        if success:
            response['success'] = True
        return Response(response, status=status.HTTP_200_OK)
    
    def response_201(self, data):
        response = {
            'success': True,
            self.label: data
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def response_400(self, data={}):
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def response_404(self):
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class APIRoot(generics.GenericAPIView):
    name = 'api-root'
    
    def get(self, request):
        return Response({
            'products': reverse('products', request=request),
            'shelfs': reverse('shelfs', request=request),
            'transports': reverse('transports', request=request),
        })


class Products(APIView, Responses):
    label = Product._meta.verbose_name
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        return self.response_200(
            serializer.data,
            success=False
        )
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return self.response_201(
                serializer.data
            )
        
        if serializer.errors.get('name'):
            return self.response_400(ERROR_NAME_TAKEN)
            
        return self.response_400(serializer.errors)


class ProductItem(APIView, Responses):
    label = Product._meta.verbose_name
    
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            
            return self.response_200(
                serializer.data,
                success=False
            )
        except Product.DoesNotExist:
            return self.response_404()
        
        return self.response_400()
    
    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
            
            product.name = request.data.get('name', product.name)
            product.quantity = request.data.get('quantity', product.quantity)
            product.save()
            
            serializer = ProductSerializer(product)
            
            return self.response_200(
                serializer.data,
                label=True
            )
        except Product.DoesNotExist:
            return self.response_404()
    
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            
            return self.response_200({})
        except Product.DoesNotExist:
            return self.response_404()

    
class Shelfs(APIView, Responses):
    label = Shelf._meta.verbose_name
    
    def get(self, request):
        shelfs = Shelf.objects.all()
        serializer = ShelfSerializer(shelfs, many=True)
        
        return self.response_200(
            serializer.data,
            success=False
        )
    
    def post(self, request):
        def create_box(box_id):
            if box_id and box_id != 'None':
                return ShelfBox.objects.get(id=box_id)
            else:
                return ShelfBox.create_empty_box()
        
        shelfs = Shelf.objects.all()
        
        if shelfs.count() < SHELF_OBJECTS_MAX_COUNT:
            box1 = create_box(request.data.get('box1'))
            box2 = create_box(request.data.get('box2'))
            box3 = create_box(request.data.get('box3'))
            
        
            shelf = Shelf.objects.create(box1=box1, box2=box2, box3=box3)
            
            serializer = ShelfSerializer(shelf)
    
            return self.response_201(
                serializer.data
            )
        
        return self.response_400(ERROR_MAX_OBJECTS)


class ShelfItem(APIView, Responses):
    label = Shelf._meta.verbose_name
    
    def get(self, request, id):
        try:
            shelf = Shelf.objects.get(id=id)
            serializer = ShelfSerializer(shelf)
            
            return self.response_200(
                serializer.data,
                success=False
            )
        except Shelf.DoesNotExist:
            return self.response_404()
        
        return self.response_400()
    
    def patch(self, request, id):
        try:
            shelf = Shelf.objects.get(id=id)
            
            for box_name in request.data:
                box = getattr(shelf, box_name)
                product_id = request.data[box_name].get('product')
                quantity = request.data[box_name].get('quantity')
                                
                if box.product.name == 'EMPTY' and box.product.id == product_id and quantity:
                    return self.response_400(ERROR_EMPTY_ARTICLE)
                else:
                    try:
                        product = Product.objects.get(id=product_id)

                        box.product = product
                        box.quantity = quantity or 0
                        box.save()
                    except Product.DoesNotExist:
                        pass
            
            serializer = ShelfSerializer(shelf)
            
            return self.response_200(
                serializer.data,
                label=True
            )
        except Shelf.DoesNotExist:
            return self.response_404()
    
    def delete(self, request, id):
        try:
            shelf = Shelf.objects.get(id=id)
            shelf.delete()
            
            return self.response_200({})
        except Shelf.DoesNotExist:
            return self.response_404()


class Transports(APIView, Responses):
    label = Transport._meta.verbose_name
    
    def get(self, request):
        transports = Transport.objects.all()
        serializer = TransportSerializer(transports, many=True)
        
        return self.response_200(
            serializer.data,
            success=False
        )
    
    def post(self, request):
        serializer = TransportSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return self.response_201(
                serializer.data
            )
        
        if serializer.errors.get('name'):
            return self.response_400(ERROR_NAME_TAKEN)
            
        return self.response_400(serializer.errors)


class TransportItem(APIView, Responses):
    label = Transport._meta.verbose_name
    
    def get(self, request, id):
        try:
            transport = Transport.objects.get(id=id)
            serializer = TransportSerializer(transport)
            
            return self.response_200(
                serializer.data,
                success=False
            )
        except Transport.DoesNotExist:
            return self.response_404()
        
        return self.response_400()
    
    def patch(self, request, id):
        try:
            transport = Transport.objects.get(id=id)
            
            transport.product_request = request.data.get(
                'product_request', transport.product_request)
            transport.status = request.data.get(
                'status', transport.status)
            transport.save()
            
            serializer = TransportSerializer(transport)
            
            return self.response_200(
                serializer.data,
                label=True
            )
        except Transport.DoesNotExist:
            return self.response_404()
    
    def delete(self, request, id):
        try:
            transport = Transport.objects.get(id=id)
            transport.delete()
            
            return self.response_200({})
        except Transport.DoesNotExist:
            return self.response_404()
        

class Prepare(APIView, Responses):
    def _save(self, *objects):
        for obj in objects:
            obj.save()
            
    def get(self, request):
        products = Product.objects.all().exclude(name='EMPTY')
        shelfs = Shelf.objects.all().iterator()
        transports = Transport.objects.all().filter(status='incoming')
        
        shelf = next(shelfs)
        box = shelf.get_free_box()
        
        for transport in transports:
            product = products.get(name=transport.product_request)
            product_available = product.get_storage()
            
            if product_available:
                free_shelf_space = shelf.get_free_space()
                
                # can't add two products to one box
                if box.product != product:
                    box = shelf.get_free_box()
                
                # shelf is full
                if not free_shelf_space or not box:
                    shelf = next(shelfs)
                    free_shelf_space = shelf.get_free_space()
                    box = shelf.get_free_box()
                
                if product_available >= CARGO_MAX_VALUE:
                    product.quantity -= CARGO_MAX_VALUE
                    
                    if box.product.name == 'EMPTY':
                        box.product = product
                    
                    if free_shelf_space >= CARGO_MAX_VALUE:
                        box.quantity += CARGO_MAX_VALUE
                    else:
                        temp = free_shelf_space
                        box.quantity += free_shelf_space
                        
                        self._save(box, shelf)
                        
                        shelf = next(shelfs)
                        free_shelf_space = shelf.get_free_space()
                        box = shelf.get_free_box()
                        
                        box.product = product
                        box.quantity += CARGO_MAX_VALUE - temp
                else:
                    product.quantity -= product_available
                    
                    if box.product.name == 'EMPTY':
                        box.product = product
                    
                    if free_shelf_space >= product_available:
                        box.quantity += product_available
                    else:
                        temp = free_shelf_space
                        box.quantity += free_shelf_space
                        
                        self._save(box, shelf)
                        
                        shelf = next(shelfs)
                        free_shelf_space = shelf.get_free_space()
                        box = shelf.get_free_box()
                        
                        box.product = product
                        box.quantity += product_available - temp
            
                
                self._save(product, box, shelf)
        
        return self.response_200({})
        
        

from django.test import TestCase

from .models import Product, ShelfBox, Transport, Shelf
from .api.serializers import ShelfBoxSerializer
from . import views
from . import example_data
from .const import *


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.name, self.quantity = example_data.PRODUCTS[0]
        self.product = Product.objects.create(
            name=self.name,
            quantity=self.quantity
        )
        
    def test_create_product_model(self):
        products = Product.objects.all()
        
        self.assertEqual(products.count(), 1)
        self.assertIsInstance(self.product, Product)
    
    def test_product_fields(self):
        self.assertTrue(hasattr(self.product, 'id'))
        self.assertEqual(self.product.name, self.name)
        self.assertEqual(self.product.quantity, self.quantity)
    
    def test_product_label(self):
        label = self.product._meta.verbose_name
        
        self.assertEqual(label, 'product')
    
    def test_empty_product(self):
        empty_product = Product.empty_product()
        
        self.assertEqual(empty_product.name, 'EMPTY')


class ShelfBoxModelTestCase(TestCase):
    def setUp(self):
        self.name, self.product_quantity = example_data.PRODUCTS[0]
        self.product = Product.objects.create(
            name=self.name,
            quantity=self.product_quantity
        )
        
        self.box_quantity = 7
        self.box = ShelfBox.objects.create(
            product=self.product,
            quantity=self.box_quantity
        )
    
    def test_create_box_model(self):
        boxes = ShelfBox.objects.all()
        
        self.assertEqual(boxes.count(), 1)
        self.assertIsInstance(self.box, ShelfBox)
    
    def test_create_empty_box(self):
        box = ShelfBox.create_empty_box()
        boxes = ShelfBox.objects.all()
        
        self.assertEqual(boxes.count(), 2)
        self.assertEqual(box.product.name, 'EMPTY')
    
    def test_box_fields(self):
        self.assertTrue(hasattr(self.box, 'id'))
        self.assertEqual(self.box.quantity, self.box_quantity)
        self.assertIsInstance(self.box.product, Product)
    
    def test_quantity_max_value(self):
        self.box.quantity = BOX_QUANTITY_MAX_VALUE + 1
        
        self.assertRaises(ValueError, self.box.save)


class ShelfBoxSerializerTestCase(TestCase):
    def setUp(self):
        self.name, self.quantity = example_data.PRODUCTS[0]
        self.product = Product.objects.create(
            name=self.name,
            quantity=self.quantity
        )
        
        self.box_quantity = 7
        self.box = ShelfBox.objects.create(
            product=self.product,
            quantity=self.box_quantity
        )
        
    def test_box_serializer(self):
        box = dict(
            id=self.box.id,
            product=self.box.product.name,
            quantity=self.box.quantity
        )
        expected_dict = example_data.box_dict(box)
        serializer = ShelfBoxSerializer(self.box)
        
        self.assertDictEqual(serializer.data, expected_dict)
    
    def test_empty_box_serializer(self):
        empty_box = ShelfBox.create_empty_box()
        
        box = dict(
            id=empty_box.id,
            product=empty_box.product.name,
            quantity=empty_box.quantity
        )
        expected_dict = example_data.box_dict(box)
        serializer = ShelfBoxSerializer(empty_box)
        
        self.assertDictEqual(serializer.data, expected_dict)


class ShelfModelTestCase(TestCase):
    def setUp(self):
        box1 = ShelfBox.objects.create()
        box2 = ShelfBox.objects.create()
        box3 = ShelfBox.objects.create()
            
        self.shelf = Shelf.objects.create(box1=box1, box2=box2, box3=box3)

    def test_create_shelf_model(self):
        shelf = Shelf.objects.all()
        
        self.assertEqual(shelf.count(), 1)
        self.assertIsInstance(self.shelf, Shelf)
    
    def test_shelf_fields(self):
        self.assertTrue(hasattr(self.shelf, 'id'))
        self.assertIsInstance(self.shelf.box1, ShelfBox)
    
    def test_shelf_label(self):
        label = self.shelf._meta.verbose_name
        
        self.assertEqual(label, 'shelf')
        

class TransportModelTestCase(TestCase):
    def setUp(self):
        self.name, _ = example_data.PRODUCTS[0]
        self.transport = Transport.objects.create(
            product_request=self.name
        )
        
    def test_create_transport_model(self):
        transport = Transport.objects.all()
        
        self.assertEqual(transport.count(), 1)
        self.assertIsInstance(self.transport, Transport)
    
    def test_transport_fields(self):
        self.assertTrue(hasattr(self.transport, 'id'))
        self.assertEqual(self.transport.product_request, self.name)
        self.assertEqual(self.transport.cargo, 0)
        self.assertEqual(self.transport.status, 'incoming')
    
    def test_transport_label(self):
        label = self.transport._meta.verbose_name
        
        self.assertEqual(label, 'transport')

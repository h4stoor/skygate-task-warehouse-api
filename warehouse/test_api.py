from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient, APITestCase

from . import example_data
from .shortcuts import TestHelpers
from .const import *


User = get_user_model()


class ProductAPITestCase(APITestCase, TestHelpers):
    def setUp(self):
        user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.api_client = APIClient()
        self.api_client.force_login(user)
        
    def test_authentication(self):
        """
         - reject unauthenticated user
         - authenticated user receives empty list
        """
        url = reverse('products')
        
        anonymous_client = APIClient()
        response = anonymous_client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'}
        )
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])

    def test_products_list(self):
        """
         - user receives list of products
        """
        products_list = self._create_products_list(self.api_client, example_data.PRODUCTS)
        
        url = reverse('products')
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), products_list)
    
    def test_add_product(self):
        """
         - user can add new product
        """
        url = reverse('products')
        data = {
            'name': 'eggs',
            'quantity': 5,
        }
        
        response = self.api_client.post(url, data=data)
        
        self.assertIn('product', response.data)
        self.assertIn('id', response.data['product'])
        
        data['id'] = response.data['product']['id']
        expected_response = {
            'success': True,
            'product': example_data.product_dict(data)
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json(), expected_response)
        
        response = self.api_client.get(url)
        expected_response = [expected_response['product']]
        
        self.assertListEqual(response.json(), expected_response)
    
    def test_unique_validator(self):
        """
         - user cannot create product with name that is already taken
        """
        url = reverse('products')
        data = {
            'name': 'eggs',
            'quantity': 5,
        }
        self.api_client.post(url, data=data)
        
        data['quantity'] = 3
        response = self.api_client.post(url, data=data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ERROR_NAME_TAKEN)
    
    def test_product_details(self):
        """
         - user receives proper info about product
        """
        product = self._create_products_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        product_id = product['id']
        expected_response = example_data.product_dict(product)
        
        url = reverse('product-item', kwargs={'id': product_id})
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)
    
    def test_update_product(self):
        """
         - user can update product
        """
        product = self._create_products_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        product_id = product['id']
        
        url = reverse('product-item', kwargs={'id': product_id})
        
        new_quantity = example_data.randint(0, example_data.MAX_STORAGE)
        product['quantity'] = new_quantity
        
        expected_response = dict(
            success=True,
            product=example_data.product_dict(product)
        )
        
        data = {'quantity': new_quantity}
        response = self.api_client.patch(url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)

    
    def test_delete_product(self):
        """
         - user can delete product
        """
        product = self._create_products_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        product_id = product['id']
        
        url = reverse('product-item', kwargs={'id': product_id})
        
        response = self.api_client.get(url)
        self.assertDictEqual(response.data, product)
        
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})
        
        url = reverse('products')
        response = self.api_client.get(url)
        
        self.assertListEqual(response.json(), [])


class ShelfAPITestCase(APITestCase, TestHelpers):
    def setUp(self):
        user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.api_client = APIClient()
        self.api_client.force_login(user)
            
    def test_authentication(self):
        """
         - reject unauthenticated user
         - authenticated user receives empty list
        """
        url = reverse('shelfs')
        
        anonymous_client = APIClient()
        response = anonymous_client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'}
        )
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])
    
    def test_add_empty_shelf(self):
        """
         - user can create empty shelf
        """
        url = reverse('shelfs')
        
        response = self.api_client.post(url, data={})
        
        self.assertIn('shelf', response.data)
        self.assertIn('box1', response.data['shelf'])
        
        box1_id, box2_id, box3_id = [
            response.data['shelf'][box]['id'] for box in ['box1', 'box2', 'box3']
        ]
        empty_shelf = {
            'id': response.data['shelf']['id'],
            'box1': {'id': box1_id, 'product': 'EMPTY'},
            'box2': {'id': box2_id, 'product': 'EMPTY'},
            'box3': {'id': box3_id, 'product': 'EMPTY'}
        }
        expected_response = {
            'success': True,
            'shelf': example_data.shelf_dict(empty_shelf)
        }

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json(), expected_response)
        
        response = self.api_client.get(url)
        expected_response = [example_data.shelf_dict(empty_shelf)]
        
        self.assertListEqual(response.json(), expected_response)
    
    def test_shelfs_list(self):
        """
         - user receives list of shelfs
        """
        products = [
            self._create_product(name, quantity).id \
            for name, quantity in example_data.PRODUCTS
        ]
        boxes = self._create_boxes(products, [1, 2, 3, 4, 5])
        boxes = [boxes[:3], boxes[3:]]
        
        shelfs_list = self._create_shelfs_list(self.api_client, boxes)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), shelfs_list)
    
    def test_maximum_shelfs(self):
        """
         - It's impossible to add more than maximum shelfs
        """
        shelfs = []
        for _ in range(SHELF_OBJECTS_MAX_COUNT):
            shelf = self._create_shelf(self.api_client)
            shelfs.append(shelf)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)
        
        self.assertEqual(len(response.json()), SHELF_OBJECTS_MAX_COUNT)
        
        response = self.api_client.post(url, data={})
        
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), ERROR_MAX_OBJECTS)
    
    def test_shelf_details(self):
        """
         - user receives proper info about shelf
        """
        products = example_data.PRODUCTS[:3]
        shelf = self._create_shelf(self.api_client, products)
        expected_response = example_data.shelf_dict(shelf)
        
        url = reverse('shelf-item', kwargs={'id': shelf['id']})
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)
    
    def test_update_shelf_1(self):
        """
         - user can update shelf
         - changing article in box
        """
        name, quantity = example_data.PRODUCTS[0]
        product = self._create_product(name, quantity)
        
        expected_dict = self._create_shelf(self.api_client)
        shelf_id = expected_dict['id']
        
        url = reverse('shelf-item', kwargs={'id': shelf_id})
        
        product_id = product.id
        new_quantity = 3
        data = {
            'box1': {
                'product': product_id,
                'quantity': new_quantity
            }
        }
        
        expected_dict['box1']['product'] = name
        expected_dict['box1']['quantity'] = new_quantity
        
        response = self.api_client.patch(url, data=data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        
        response_dict = response.json()['shelf']
        
        self.assertDictEqual(response_dict, expected_dict)

    
    def test_delete_shelf(self):
        """
         - user can delete shelf
        """
        products = example_data.PRODUCTS[:3]
        shelf = self._create_shelf(self.api_client, products)
        
        url = reverse('shelf-item', kwargs={'id': shelf['id']})
        
        response = self.api_client.get(url)
        self.assertDictEqual(response.data, shelf)
        
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})
        
        url = reverse('shelfs')
        response = self.api_client.get(url)
        
        self.assertListEqual(response.json(), [])


class TransportAPITestCase(APITestCase, TestHelpers):
    def setUp(self):
        user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.api_client = APIClient()
        self.api_client.force_login(user)
        
    def test_authentication(self):
        """
         - reject unauthenticated user
         - authenticated user receives empty list
        """
        url = reverse('transports')
        
        anonymous_client = APIClient()
        response = anonymous_client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'}
        )
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])

    def test_transports_list(self):
        """
         - user receives list of transports
        """
        transports_list = self._create_transports_list(self.api_client, example_data.PRODUCTS)
        
        url = reverse('transports')
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), transports_list)
    
    def test_add_transport(self):
        """
         - user can add new transport
        """
        url = reverse('transports')
        data = {
            'product_request': 'eggs',
            'cargo': 5,
            'status': 'done'
        }
        
        response = self.api_client.post(url, data=data)
        
        self.assertIn('transport', response.data)
        self.assertIn('id', response.data['transport'])
        
        data['id'] = response.data['transport']['id']
        expected_response = {
            'success': True,
            'transport': example_data.transport_dict(data)
        }

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json(), expected_response)
        
        response = self.api_client.get(url)
        
        expected_response = [expected_response['transport']]
        
        self.assertListEqual(response.json(), expected_response)
    
    def test_transport_details(self):
        """
         - user receives proper info about transport
        """
        transport = self._create_transports_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        transport_id = transport['id']
        expected_response = example_data.transport_dict(transport)
        
        url = reverse('transport-item', kwargs={'id': transport_id})
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)
    
    def test_update_transport(self):
        """
         - user can update transport
        """
        transport = self._create_transports_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        transport_id = transport['id']
        
        url = reverse('transport-item', kwargs={'id': transport_id})
        
        new_product_request = example_data.PRODUCTS[1][0]
        new_status = 'loading'
        transport['product_request'] = new_product_request
        transport['status'] = new_status
        
        expected_response = dict(
            success=True,
            transport=example_data.transport_dict(transport)
        )
        
        data = {
            'product_request': new_product_request,
            'status': new_status
        }
        response = self.api_client.patch(url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)

    
    def test_delete_transport(self):
        """
         - user can delete transport
        """
        transport = self._create_transports_list(
            self.api_client,
            [example_data.PRODUCTS[0]]
        )[0]
        transport_id = transport['id']
        
        url = reverse('transport-item', kwargs={'id': transport_id})
        
        response = self.api_client.get(url)
        self.assertDictEqual(response.data, transport)
        
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})
        
        url = reverse('transports')
        response = self.api_client.get(url)
        
        self.assertListEqual(response.json(), [])

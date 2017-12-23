from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient, APITestCase

from . import example_data


User = get_user_model()


class SolutionTest(APITestCase):
    def _products(self, products):
        url = reverse('products')
        for name, quantity in products:
            data = {
                'name': name,
                'quantity': quantity
            }
            self.api_client.post(url, data=data)
    
    def _transports(self, transports):
        url = reverse('transports')
        for product in transports:
            data = {
                'product_request': product
            }
            self.api_client.post(url, data=data)
    
    def _shelfs(self):
        url = reverse('shelfs')
        shelfs = []
        for _ in range(10):
            response = self.api_client.post(url, data={})
            shelfs.append(response.json()['shelf'])
        
        url = reverse('shelfs-prepare')
        response = self.api_client.get(url)
        return shelfs
            
    def setUp(self):
        user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.api_client = APIClient()
        self.api_client.force_login(user)
        
        #create 10 empty shelfs
        url = reverse('shelfs')
        self.shelfs = []
        for _ in range(10):
            response = self.api_client.post(url, data={})
            self.shelfs.append(response.json()['shelf'])
        
    def test_computing_with_max_storage(self):
        """
         - validate proper prepering shelfs for products with max storage
        """
        self._products(example_data.SOLUTION_PRODUCTS_DATA_1)
        self._transports(example_data.SOLUTION_TRANSPORTS_DATA_1)
                
        url = reverse('shelfs-prepare')
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)
        
        self.assertListEqual(response.json(), example_data.SOLUTION_SHELFS_DATA_1)
    
    def test_computing_with_no_storage(self):
        """
         - validate proper prepering shelfs for products with no storage
        """
        self._products(example_data.SOLUTION_PRODUCTS_DATA_2)
        self._transports(example_data.SOLUTION_TRANSPORTS_DATA_2)
        
        url = reverse('shelfs-prepare')
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)
        
        self.assertListEqual(response.json(), self.shelfs)
        
    def test_computing_with_various_storage(self):
        """
         - validate proper prepering shelfs for products with various storage
        """
        self._products(example_data.SOLUTION_PRODUCTS_DATA_3)
        self._transports(example_data.SOLUTION_TRANSPORTS_DATA_3)
        
        url = reverse('shelfs-prepare')
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)

        self.assertListEqual(response.json(), example_data.SOLUTION_SHELFS_DATA_3)
    
    def test_computing_big_transports(self):
        """
         - validate proper prepering shelfs for big amount of transports
        """
        self._products(example_data.SOLUTION_PRODUCTS_DATA_4)
        self._transports(example_data.SOLUTION_TRANSPORTS_DATA_4)
        
        url = reverse('shelfs-prepare')
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        url = reverse('shelfs')
        response = self.api_client.get(url)
            
        self.assertListEqual(response.json(), example_data.SOLUTION_SHELFS_DATA_4)


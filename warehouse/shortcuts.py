from django.core.urlresolvers import reverse

from .models import Product, ShelfBox, Transport


class TestHelpers:
    def _create_product(self, name, quantity):
        """
         Create Product object
         :return: Product instance
        """
        product = Product.objects.create(
            name = name,
            quantity = quantity
        )
        return product

    def _create_products_list(self, api_client, products):
        """
         Creates example products using api_client
         :products: list of products in format [(name, quantity)]
         :return: list of products created by API
        """
        products_list = []
        url = reverse('products')
        for name, quantity in products:
            data = dict(
                name = name,
                quantity = quantity,
            )
            response = api_client.post(url, data=data)
            products_list.append(response.data['product'])
        return products_list

    def _create_box(self, product_id, quantity):
        """
         Create ShelfBox object
         :product_id: Product instance id
         :return: ShelfBox instance
        """
        product = Product.objects.get(id=product_id)
        box = ShelfBox.objects.create(
            product = product,
            quantity = quantity
        )
        return box
    
    def _create_transport(self, product_name):
        """
         Create Transport objects
        """
        transport = Transport.objects.create(product_request=product_name)
        return transport
    
    def _create_boxes(self, products_id, quantities):
        """
         Create multiple ShelfBox objects
        """
        boxes_id = []
        for product_id, quantity in zip(products_id, quantities):
            box = self._create_box(product_id, quantity)
            boxes_id.append(box.id)
        return boxes_id
    
    def _create_shelf(self, api_client, products=None):
        """
         Creates example shelf using api client
         :return: shelf dict created by api
        """
        products = []
        for product in products:
            if product:
                name, quantity = product
                product = self._create_product(name, quantity).id
            else:
                product = Product.empty_product().id
            products.append(product)
        boxes = self._create_boxes(products, [1, 2, 3])
        shelf = self._create_shelfs_list(
            api_client,
            [boxes]
        )[0]
        shelf_id = shelf['id']
        return shelf
                    
    def _create_shelfs_list(self, api_client, shelfs):
        """
         Creates example shelfs using api client
         :shelfs: list of shelfs in format [(box1.id, box2.id, box3.id)]
         :return: list of shelfs created by API
        """
        shelfs_list = []
        url = reverse('shelfs')
        for boxes in shelfs:
            if len(boxes) < 3:
                boxes = list(boxes) + [None] * (3 - len(boxes))
            box1_id, box2_id, box3_id = boxes
            data = dict(
                box1 = box1_id,
                box2 = box2_id,
                box3 = box3_id
            )
            response = api_client.post(url, data=data)
            shelfs_list.append(response.data['shelf'])
        return shelfs_list
    
    def _create_transports_list(self, api_client, products):
        transports_list = []
        url = reverse('transports')
        for product_request, _ in products:
            data = dict(
                product_request=product_request,
                cargo=0,
                status='incoming'
            )
            response = api_client.post(url, data=data)
            transports_list.append(response.data['transport'])
        return transports_list

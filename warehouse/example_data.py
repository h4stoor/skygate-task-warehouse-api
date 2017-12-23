from random import randint

    
def product_dict(product):
    product_dict = BASE_PRODUCT_DICT.copy()
    product_dict['id'] = product.get('id')
    product_dict['name'] = product.get('name')
    product_dict['quantity'] = product.get('quantity') or 0
    return product_dict

def products_list(products):
    return [product_dict(product) for product in products]

def box_dict(box):
    box_dict = BASE_BOX_DICT.copy()
    box_dict['id'] = box.get('id')
    box_dict['product'] = box.get('product')
    box_dict['quantity'] = box.get('quantity') or 0
    return box_dict

def shelf_dict(shelf):
    shelf_dict = BASE_SHELF_DICT.copy()
    shelf_dict['id'] = shelf.get('id')
    shelf_dict['box1'] = box_dict(shelf.get('box1'))
    shelf_dict['box2'] = box_dict(shelf.get('box2'))
    shelf_dict['box3'] = box_dict(shelf.get('box3'))
    return shelf_dict

def transport_dict(transport):
    transport_dict = BASE_TRANSPORT_DICT.copy()
    transport_dict['id'] = transport.get('id')
    transport_dict['product_request'] = transport.get('product_request')
    transport_dict['cargo'] = transport.get('cargo')
    transport_dict['status'] = transport.get('status')
    return transport_dict

MAX_STORAGE = 20

PRODUCTS = [
    ('christmas tree', MAX_STORAGE),
    ('sword', MAX_STORAGE),
    ('notebook', MAX_STORAGE),
    ('chips', MAX_STORAGE),
    ('bike', MAX_STORAGE),
]

BASE_PRODUCT_DICT = {
    'id': None,
    'name': None,
    'quantity': 0,
}

BASE_BOX_DICT = {
    'id': None,
    'product': BASE_PRODUCT_DICT,
    'quantity': None
}

BASE_SHELF_DICT = {
    'id': None,
    'box1': BASE_BOX_DICT,
    'box2': BASE_BOX_DICT,
    'box3': BASE_BOX_DICT
}

BASE_TRANSPORT_DICT = {
    'id': None,
    'product_request': None,
    'cargo': None,
    'status': None
}

SOLUTION_PRODUCTS_DATA_1 = PRODUCTS.copy()
SOLUTION_TRANSPORTS_DATA_1 = ['christmas tree', 'sword', 'notebook', 'chips', 'bike'] * 2
SOLUTION_SHELFS_DATA_1 = [
     {'box1': {'id': 1, 'product': 'christmas tree', 'quantity': 5},
      'box2': {'id': 2, 'product': 'sword', 'quantity': 5},
      'box3': {'id': 3, 'product': 'EMPTY', 'quantity': 0},
      'id': 1},
     {'box1': {'id': 4, 'product': 'notebook', 'quantity': 5},
      'box2': {'id': 5, 'product': 'chips', 'quantity': 5},
      'box3': {'id': 6, 'product': 'EMPTY', 'quantity': 0},
      'id': 2},
     {'box1': {'id': 7, 'product': 'bike', 'quantity': 5},
      'box2': {'id': 8, 'product': 'christmas tree', 'quantity': 5},
      'box3': {'id': 9, 'product': 'EMPTY', 'quantity': 0},
      'id': 3},
     {'box1': {'id': 10, 'product': 'sword', 'quantity': 5},
      'box2': {'id': 11, 'product': 'notebook', 'quantity': 5},
      'box3': {'id': 12, 'product': 'EMPTY', 'quantity': 0},
      'id': 4},
     {'box1': {'id': 13, 'product': 'chips', 'quantity': 5},
      'box2': {'id': 14, 'product': 'bike', 'quantity': 5},
      'box3': {'id': 15, 'product': 'EMPTY', 'quantity': 0},
      'id': 5},
     {'box1': {'id': 16, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 17, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 18, 'product': 'EMPTY', 'quantity': 0},
      'id': 6},
     {'box1': {'id': 19, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 20, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 21, 'product': 'EMPTY', 'quantity': 0},
      'id': 7},
     {'box1': {'id': 22, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 23, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 24, 'product': 'EMPTY', 'quantity': 0},
      'id': 8},
     {'box1': {'id': 25, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 26, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 27, 'product': 'EMPTY', 'quantity': 0},
      'id': 9},
     {'box1': {'id': 28, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 29, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 30, 'product': 'EMPTY', 'quantity': 0},
      'id': 10}
]

SOLUTION_PRODUCTS_DATA_2 = [(product, 0) for product, _ in PRODUCTS]
SOLUTION_TRANSPORTS_DATA_2 = ['christmas tree', 'sword', 'notebook', 'chips', 'bike'] * 2

SOLUTION_PRODUCTS_DATA_3 = [
    ('christmas tree', 8),
    ('sword', 14),
    ('notebook', 0),
    ('chips', 11),
    ('bike', 4)
]
SOLUTION_TRANSPORTS_DATA_3 = [
    'christmas tree',
    'christmas tree',
    'sword',
    'bike',
    'notebook',
    'chips',
    'chips',
    'chips',
    'bike',
    'sword'
]
SOLUTION_SHELFS_DATA_3 = [
     {'box1': {'id': 1, 'product': 'christmas tree', 'quantity': 8},
      'box2': {'id': 2, 'product': 'sword', 'quantity': 2},
      'box3': {'id': 3, 'product': 'EMPTY', 'quantity': 0},
      'id': 1},
     {'box1': {'id': 4, 'product': 'sword', 'quantity': 3},
      'box2': {'id': 5, 'product': 'bike', 'quantity': 4},
      'box3': {'id': 6, 'product': 'chips', 'quantity': 3},
      'id': 2},
     {'box1': {'id': 7, 'product': 'chips', 'quantity': 8},
      'box2': {'id': 8, 'product': 'sword', 'quantity': 2},
      'box3': {'id': 9, 'product': 'EMPTY', 'quantity': 0},
      'id': 3},
     {'box1': {'id': 10, 'product': 'sword', 'quantity': 3},
      'box2': {'id': 11, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 12, 'product': 'EMPTY', 'quantity': 0},
      'id': 4},
     {'box1': {'id': 13, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 14, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 15, 'product': 'EMPTY', 'quantity': 0},
      'id': 5},
     {'box1': {'id': 16, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 17, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 18, 'product': 'EMPTY', 'quantity': 0},
      'id': 6},
     {'box1': {'id': 19, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 20, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 21, 'product': 'EMPTY', 'quantity': 0},
      'id': 7},
     {'box1': {'id': 22, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 23, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 24, 'product': 'EMPTY', 'quantity': 0},
      'id': 8},
     {'box1': {'id': 25, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 26, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 27, 'product': 'EMPTY', 'quantity': 0},
      'id': 9},
     {'box1': {'id': 28, 'product': 'EMPTY', 'quantity': 0},
      'box2': {'id': 29, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 30, 'product': 'EMPTY', 'quantity': 0},
      'id': 10}
]

SOLUTION_PRODUCTS_DATA_4 = [
    ('christmas tree', 18),
    ('sword', 19),
    ('notebook', 17),
    ('chips', 15),
    ('bike', 23)
]
SOLUTION_TRANSPORTS_DATA_4 = ['christmas tree', 'sword', 'notebook', 'chips', 'bike'] * 6
SOLUTION_SHELFS_DATA_4 = [
     {'box1': {'id': 1, 'product': 'christmas tree', 'quantity': 5},
      'box2': {'id': 2, 'product': 'sword', 'quantity': 5},
      'box3': {'id': 3, 'product': 'EMPTY', 'quantity': 0},
      'id': 1},
     {'box1': {'id': 4, 'product': 'notebook', 'quantity': 5},
      'box2': {'id': 5, 'product': 'chips', 'quantity': 5},
      'box3': {'id': 6, 'product': 'EMPTY', 'quantity': 0},
      'id': 2},
     {'box1': {'id': 7, 'product': 'bike', 'quantity': 5},
      'box2': {'id': 8, 'product': 'christmas tree', 'quantity': 5},
      'box3': {'id': 9, 'product': 'EMPTY', 'quantity': 0},
      'id': 3},
     {'box1': {'id': 10, 'product': 'sword', 'quantity': 5},
      'box2': {'id': 11, 'product': 'notebook', 'quantity': 5},
      'box3': {'id': 12, 'product': 'EMPTY', 'quantity': 0},
      'id': 4},
     {'box1': {'id': 13, 'product': 'chips', 'quantity': 5},
      'box2': {'id': 14, 'product': 'bike', 'quantity': 5},
      'box3': {'id': 15, 'product': 'EMPTY', 'quantity': 0},
      'id': 5},
     {'box1': {'id': 16, 'product': 'christmas tree', 'quantity': 5},
      'box2': {'id': 17, 'product': 'sword', 'quantity': 5},
      'box3': {'id': 18, 'product': 'EMPTY', 'quantity': 0},
      'id': 6},
     {'box1': {'id': 19, 'product': 'notebook', 'quantity': 5},
      'box2': {'id': 20, 'product': 'chips', 'quantity': 5},
      'box3': {'id': 21, 'product': 'EMPTY', 'quantity': 0},
      'id': 7},
     {'box1': {'id': 22, 'product': 'bike', 'quantity': 5},
      'box2': {'id': 23, 'product': 'christmas tree', 'quantity': 3},
      'box3': {'id': 24, 'product': 'sword', 'quantity': 2},
      'id': 8},
     {'box1': {'id': 25, 'product': 'sword', 'quantity': 2},
      'box2': {'id': 26, 'product': 'notebook', 'quantity': 2},
      'box3': {'id': 27, 'product': 'bike', 'quantity': 6},
      'id': 9},
     {'box1': {'id': 28, 'product': 'bike', 'quantity': 2},
      'box2': {'id': 29, 'product': 'EMPTY', 'quantity': 0},
      'box3': {'id': 30, 'product': 'EMPTY', 'quantity': 0},
      'id': 10}
]

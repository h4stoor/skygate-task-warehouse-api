#### Description

>W nowoczesnym magazynie znajduje się 10 autonomicznych półek ustawionych w jednej linii do ładowni ciężarówek.<br>
>Półki te potrafią same się przestawiać, dzięki czemu możliwy jest szybszy dostęp do zamówionych produktów.<br>
>
>Półki ustawiają się samoczynnie w nocy. Kiedy w trakcie ładunku towarów jest konieczna zmiana ustawień półek,<br>
>półki mogą przesunąć się tylko do przodu, a półka znajdująca się na początku wędruje na koniec<br>
>(jak w przypadku kolejki cyklicznej)<br>
>
>Na każdej półce znajduje się miejsce na 10 jednostek spośród jednego do trzech z 5 typów produktów.<br>
>(Dla przykładu półka posiadająca 7 jednostek jabłek i 3 jednostki pomarańczy)<br>
>Do magazynu codziennie przyjeżdżają odbiorcy towaru w z góry zaplanowanej kolejności (10 transportów).<br>
>
>Każdy transport stara się zabrać 5 jednostek jednego typu produktu, po który przyjechał. Ciężarówka transportowa<br>
>nie będzie nigdy żądać jednocześnie kilku typów produktów lub innej ilości niż 5 jednostek.<br>
>
>W przypadku kiedy w magazynie zabraknie danego typu towaru, transport odjedzie niepełny lub pusty.<br>
>
>W nocy półki powinny sortować się w taki sposób, aby czas załadunku wszystkich ciężarówek był w sumie jak najkrótszy.<br>
>Korzystając z django rest framework, flask, dowolnego innego frameworka lub czystego języka pythona napisz aplikację, która:<br>
>- umożliwi tworzenie, aktualizowanie i usuwanie typów towarów, półek i transportów<br>
>- pozwoli pobrać przez frontend listę półek wraz z ich zawartością oraz listę transportów<br>
>- przy pobraniu listy półek otrzymamy na miarę własnych możliwości optymalnie posortowane półki w taki sposób,<br>
>aby obsłużyć wszystkie transporty z jak najmniejszą ilością przesunięć półek<br>
>
>W zadaniu należy wykorzystać relacyjną bazę danych, stworzyć odpowiednie modele oraz relacje.<br>
>
>Kod powinien posiadać testy jednostkowe i integracyjne tam, gdzie jest to potrzebne (z wykorzystaniem mocków jeśli jest to niezbędne)<br>
>
>Proszę się nie przejmować, jeżeli zaimplementowany algorytm nie będzie bardzo optymalny, dla nas ważniejsza jest<br>
>umiejętność rozwiązywania problemów, nie chcielibyśmy aby poszukiwanie idealnego rozwiązania sprawiło, że projekt<br>
>nie zostałby ukończony :)<br>

#### Setup
```
mkdir <project_dir> && cd <project_dir>
virtualenv -p python3 .
source bin/activate
git init
git clone https://github.com/h4stoor/python-skygate-task.git src
cd src
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

# WAREHOUSE API

## `/api/`
**GET** - Root.

### `/product/`
**GET** - List of all products.
**POST** - Add product.
#### `/{id}`
**GET** - Info about product.
**PATCH** - Update product.
**DELETE** - Delete product.

### `/shelf/`
**GET** - List of all shelfs.
**POST** - Create shelf.
#### `/prepare/` - TASK SOLVER.
#### `/{id}`
**GET** - Info about shelf.
**PATCH** - Update shelf.
**DELETE** - Delete shelf.

### `/transport/`
**GET** - List of all transports.
**POST** - Create transport.
#### `/{id}`
**GET** - Info about transport.
**PATCH** - Update transport.
**DELETE** - Delete transport.


## API `/api`

### `/product/`

**GET**

List of all products.

```json
[
    {
        "id": 1,
        "name": "product1",
        "quantity": 16,
    },
    {
        "id": 2,
        "name": "product2",
        "quantity": 21,
    },
    {
        "id": 3,
        "name": "product3",
        "quantity": 3,
    },
]
```

**POST**

Add an product.

```json
{
    "name": "product4",
    "quantity": 7
}
```

*returns*
```json
{
    "success": true,
    "product": {
        "id": 4,
        "name": "product4",
        "quantity": 7
    }
}
```

#### `/{id}`

**GET**

Info about an product.

```json
{
    "id": 2
    "name": "product2",
    "quantity": 21
}
```

**PATCH**

Update an product.

```json
{
    "name": "other",
    "quantity": 8
}
```

*returns*
```json
{
    "success": true,
    "product": {
        "id": 2,
        "name": "other",
        "quantity": 8
    }
}
```

**DELETE**

Delete an product.

```json
{
    "success": true
}
```


### `/shelf/`

**GET**

List of all shelfs.

```json
[
    {
        'box1': {
            'id': 1,
            'product': 'product1',
            'quantity': 8
        },
        'box2': {
            'id': 2,
            'product': 'product2',
            'quantity': 2
        },
        'box3': {
            'id': 3,
            'product': 'EMPTY',
            'quantity': 0
        },
        'id': 1
    },
    {
        'box1': {
            'id': 4,
            'product': 'product2',
            'quantity': 3
        },
        'box2': {
            'id': 5,
            'product': 'product3',
            'quantity': 4
        },
        'box3': {
            'id': 6,
            'product': 'product1',
            'quantity': 3
        },
        'id': 2},
]
```

**POST**

Create a shelve

```json
{}
```

*returns*

```json
{
    "success": true,
    "shelf": {
        "id": 3,
        "box1": {
            "id": 7,
            "product": "EMPTY",
            "quantity": 0
        },
        "box2": {
            "id": 8,
            "product": "EMPTY",
            "quantity": 0
        },
        "box3": {
            "id": 9,
            "product": "EMPTY",
            "quantity": 0
        }
    }
}
```

### `/prepare/`

**GET**

TASK SOLVER

```json
[
    {
        'box1': {
            'id': 1,
            'product': 'product1',
            'quantity': 8
        },
        'box2': {
            'id': 2,
            'product': 'product2',
            'quantity': 2
        },
        'box3': {
            'id': 3,
            'product': 'EMPTY',
            'quantity': 0
        },
        'id': 1
    },
    {
        'box1': {
            'id': 4,
            'product': 'product2',
            'quantity': 3
        },
        'box2': {
            'id': 5,
            'product': 'product3',
            'quantity': 4
        },
        'box3': {
            'id': 6,
            'product': 'product5',
            'quantity': 3
        },
        'id': 2
    },
    {
        'box1': {
            'id': 7,
            'product': 'product4',
            'quantity': 8
        },
        'box2': {
            'id': 8,
            'product': 'product7',
            'quantity': 2
        },
        'box3': {
            'id': 9,
            'product': 'EMPTY',
            'quantity': 0
        },
        'id': 3
    },
...
]
```

#### `/{id}`

**GET**

Info about shelve.

```json
{
    "id": 3,
    "box1": {
        "id": 7,
        "product": "product1",
        "quantity": 3
    },
    "box2": {
        "id": 8,
        "product": "product2",
        "quantity": 7
    },
    "box3": {
        "id": 9,
        "product": "EMPTY",
        "quantity": 0
    }
}
```

**PATCH**

Update shelve.

```json
{
    "box1": {
        "product": 2,
        "quantity": 1
    }
}
```

*returns*
```json
{
    "success": true,
    "shelf": {
        "id": 3,
        "box1": {
            "id": 7,
            "product": "product2",
            "quantity": 1
        },
        "box2": {
            "id": 8,
            "product": "EMPTY",
            "quantity": 0
        },
        "box3": {
            "id": 9,
            "product": "EMPTY",
            "quantity": 0
        }
    }
}
```

**DELETE**

Delete a shelve.

```json
{
    "success": true
}
```


### `/transport/`

**GET**

List of all transports.

```json
[
    {
        "id": 1,
        "product_request": "product2",
        "cargo": 0,
        "status": "incoming"
    },
    {
        "id": 2,
        "product_request": "product1",
        "cargo": 0,
        "status": "incoming"
    },
    {
        "id": 3,
        "product_request": "product3",
        "cargo": 0,
        "status": "incoming"
    }
]
```

**POST**

Create a transport.

```json
{
    "product_request": "product4"
}
```

*returns*
```json
{
    "success": true,
    "transport": {
        "id": 4,
        "product_request": "product4",
        "cargo": 0,
        "status": "incoming"
    }
}
```
#### `/{id}`

**GET**

Info about transport.

```json
{
    "id": 2,
    "product_request": "product1",
    "cargo": 0,
    "status": "incoming"
}
```

**PATCH**

Update transport.

```json
{
    "product_request": "product4",
    "status": "waiting"
}
```

*returns*
```json
{
    "success": true,
    "transport": {
        "id": 2,
        "product_request": "product4",
        "cargo": 0,
        "status": "waiting"
    }
}
```

**DELETE**

Delete transport.

```json
{
    "success": true
}
```

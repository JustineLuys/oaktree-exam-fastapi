from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from routers.api import get_db
from utils.auth import get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from models import Items
import pytest 

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args= {'check_same_thread': False}, 
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'justinezxc', 'id': 1}
     
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_items():
    item = Items(
        name="Louis Vuitton",
        description="My new luxury bag",
        price=500,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(item)
    db.commit()
    yield item
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM items;"))
        connection.commit()
    
def test_get_all_items_authenticated(test_items):
    response = client.get('/api/items')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'data': [
            {
                'id': 1,
                'name': 'Louis Vuitton',
                'description': 'My new luxury bag',
                'price': 500,
                'owner_id': 1
            }
        ]
    }

def test_get_item_authenticated(test_items):
    response = client.get('/api/items/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'data': {
                'id': 1,
                'name': 'Louis Vuitton',
                'description': 'My new luxury bag',
                'price': 500,
                'owner_id': 1
            }
    }

def test_get_item_authenticated_not_found(test_items):
    response = client.get('/api/items/500')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item with id 500 is not found'}

def test_create_item(test_items):
    request_data={
        'name': 'New Item',
        'description': 'New item description',
        'price': 400,
    }
    
    response = client.post('/api/items', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Items).filter(Items.id == 2).first()
    assert model.name == request_data.get('name')
    assert model.description == request_data.get('description')
    assert model.price == request_data.get('price')

def test_update_item(test_items):
    request_data={
        'name': 'New Item Updated',
        'description': 'New item description updated',
        'price': 400,
    }
    
    response = client.put('/api/items/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Items).filter(Items.id == 1).first()
    assert model.name == request_data.get('name')

def test_update_item_not_found(test_items):
    request_data={
        'name': 'New Item Updated',
        'description': 'New item description updated',
        'price': 400,
    }
    response = client.put('/api/items/500', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item with id 500 is not found'}
    
def test_delete_item(test_items):
    response = client.delete('/api/items/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Items).filter(Items.id == 1).first()
    assert model is None

def test_delete_item_not_found(test_items):
    response = client.delete('/api/items/500')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item with id 500 is not found'}
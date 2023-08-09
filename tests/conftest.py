import pytest
from ActualBackend.models import *
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def user_data():
    user = User.objects.create(
        username='test_user',
        email='testuser@example.com',
        password='testuserpassword',
        role='user'
    )
    return user

@pytest.fixture
def admin_data():
    user = User.objects.create(
        username='test_admin',
        email='testadmin@example.com',
        password='testAdminpassword',
        role='admin'
    )
    return user

@pytest.fixture
def user_data1():
    user = {
        "username": "test_user",
        "email": "testuser@example.com",
        "password": "testuserpassword",
        "role": "user"
    }
    return user

@pytest.fixture
def user_data2():
    user = {
        "username": "test_user",
        "email": "testuser@example.com",
        "password": "testuserpassword",
        "role": "User"
    }
    return user


@pytest.fixture
def user_login_data1():
    user = {
        "email": "testuser@example.com",
        "password": "testuserpassword",
    }
    return user


@pytest.fixture
def travel_plan_data():
    with open("/Users/consultadd/Downloads/sunny-weather-vector-12210439.jpg", "rb") as f:
        image_data = f.read()
    return {
        'name': 'Test Plan',
        'description': 'Test Description',
        'price': 100.0,
        'image': SimpleUploadedFile("sunny-weather-vector-12210439.jpg", image_data, content_type="image/jpg"),
        'start_date': "2023-08-01",
        'end_date': "2023-08-05",
        'registered_admin_id': 1
    }

@pytest.fixture
def travel_plan_data2():
    with open("/Users/consultadd/Downloads/sunny-weather-vector-12210439.jpg", "rb") as f:
        image_data = f.read()
    return {
        'name': 'Test Plan',
        'description': 'Test Description',
        'price': 100.0,
        'image': SimpleUploadedFile("sunny-weather-vector-12210439.jpg", image_data, content_type="image/jpg"),
        'start_date': "2023-08-02",
        'end_date': "2023-08-01",
        'registered_admin_id': 1
    }


@pytest.fixture
def registered_plan_data():
    admin_user = User.objects.create(
        username='admin_user',
        email='admin@example.com',
        password='adminpassword',
        role='admin'
    )

    travel_plan = TravelPlans.objects.create(
        name='Test Plan',
        description='Test Description',
        price=100.0,
        start_date=date(2023, 8, 1),
        end_date=date(2023, 8, 5),
        registered_admin_id=admin_user.id
    )

    user = User.objects.create(
        username='test_user',
        email='test@example.com',
        password='testpassword',
        role='user'
    )

    return {'user': user, 'travel_plan': travel_plan}


@pytest.fixture
def registered_plan_create(registered_plan_data):
    registered_plan = RegisteredPlans.objects.create(
        userID=registered_plan_data['user'],
        planID=registered_plan_data['travel_plan']
    )
    return {'registered_plan': registered_plan}

@pytest.fixture
def travel_all_plans_fixture():
    with open("/Users/consultadd/Downloads/sunny-weather-vector-12210439.jpg", "rb") as f:
        image_data = f.read()
    return [
        {
            'name': 'Plan 1',
            'description': 'Description for Plan 1',
            'price': 100.0,
            'image': SimpleUploadedFile("sunny-weather-vector-12210439.jpg", image_data, content_type="image/jpg"),
            'start_date': "2023-08-01",
            'end_date': "2023-08-05",
            'registered_admin_id': 1,
        },
        {
            {
                'name': 'Plan 2',
                'description': 'Description for Plan 2',
                'price': 200.0,
                'image': SimpleUploadedFile("sunny-weather-vector-12210439.jpg", image_data, content_type="image/jpg"),
                'start_date': "2023-08-06",
                'end_date': "2023-08-10",
                'registered_admin_id': 2,
            }
        }
    ]

@pytest.fixture
def modify_dates():
    return {
        'start_dates' : '2023-08-10',
        'end_dates' : '2023-08-11'
    }

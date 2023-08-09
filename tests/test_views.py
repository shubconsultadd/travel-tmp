import pytest
from ActualBackend.models import *
from django.urls import reverse
from datetime import date
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_user_registration_api1(user_data1):
    client = APIClient()
    response = client.post('/backend/register', user_data1, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    assert response.data['username'] == user_data1['username']
    assert response.data['email'] == user_data1['email']
    assert response.data['role'] == user_data1['role']

    user = User.objects.get()
    assert user.username == user_data1['username']
    assert user.email == user_data1['email']
    assert user.role == user_data1['role']


@pytest.mark.django_db
def test_user_registration_api2(user_data2):
    client = APIClient()
    response = client.post('/backend/register', user_data2, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_user_login_api1(user_data1):
    client = APIClient()

    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    response = client.post('/backend/login', user_data1, format='json')

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_travel_plan(travel_plan_data):
    client = APIClient()

    response = client.post('/backend/add_plan', travel_plan_data)

    assert response.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1
    assert 'message' in response.data
    assert response.data['message'] == "Created Travel Plan"
    assert 'start_date' in response.data
    assert 'end_date' in response.data


@pytest.mark.django_db
def test_add_wrong_travel_plan(travel_plan_data2):
    client = APIClient()

    response = client.post('/backend/add_plan', travel_plan_data2)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_all_travel_plans(travel_plan_data):
    client = APIClient()

    response1 = client.post('/backend/add_plan', travel_plan_data)

    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.get('/backend/get_plans')

    assert response2.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_plan(travel_plan_data):
    client = APIClient()

    response1 = client.post('/backend/add_plan', travel_plan_data)

    assert response1.status_code == status.HTTP_201_CREATED

    plan_id = response1.data['id']

    url = reverse('delete-plan', args=[plan_id, travel_plan_data['registered_admin_id']])
    response2 = client.delete(url)

    assert response2.status_code == status.HTTP_204_NO_CONTENT
    assert 'message' in response2.data


@pytest.mark.django_db
def test_delete_plan2(travel_plan_data):
    client = APIClient()

    response1 = client.post('/backend/add_plan', travel_plan_data)

    assert response1.status_code == status.HTTP_201_CREATED

    plan_id = response1.data['id']

    url = reverse('delete-plan', args=[plan_id, 0])
    response2 = client.delete(url)

    assert response2.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_register_plan(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED


@pytest.mark.xfail
@pytest.mark.django_db
def test_register_plan2(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': 0
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_deregister_plan(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED

    url = reverse('de-register', args=[response1.data['id'], response3.data['id']])

    response5 = client.delete(url)
    assert response5.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_registered_plans(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED

    url = reverse('user-plans', args=[response1.data['id']])

    response5 = client.get(url)
    assert response5.status_code == status.HTTP_200_OK


@pytest.mark.xfail
@pytest.mark.django_db
def test_user_registered_plans2(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED

    url = reverse('user-plans', args=[2])

    response5 = client.get(url)
    assert response5.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_is_user_registered_with_the_plan(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED

    url = reverse('is-user', args=[response1.data['id'], response3.data['id']])

    response5 = client.get(url)

    assert response5.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_modify_travel_plan(travel_plan_data, modify_dates):
    client = APIClient()

    response1 = client.post('/backend/add_plan', travel_plan_data)

    assert response1.status_code == status.HTTP_201_CREATED

    planID = response1.data['id']

    url = reverse('modify-plan', args=[planID])

    response2 = client.put(url, modify_dates)

    assert response2.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_show_plans_with_registeredUsers(travel_plan_data, user_data1):
    client = APIClient()
    response1 = client.post('/backend/register', user_data1, format='json')

    assert response1.status_code == status.HTTP_201_CREATED

    assert User.objects.count() == 1

    response2 = client.post('/backend/login', user_data1, format='json')

    assert response2.status_code == status.HTTP_201_CREATED

    response3 = client.post('/backend/add_plan', travel_plan_data)

    assert response3.status_code == status.HTTP_201_CREATED

    assert TravelPlans.objects.count() == 1

    data = {
        'userID': response1.data['id'],
        'planID': response3.data['id']
    }

    response4 = client.post('/backend/register_plan', data)

    assert response4.status_code == status.HTTP_201_CREATED

    planID = response3.data['id']

    url = reverse('show-plan', args=[planID])

    response5 = client.get(url)

    assert response5.status_code == status.HTTP_200_OK

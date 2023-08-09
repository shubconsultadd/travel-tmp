import pytest
from ActualBackend.models import *
from datetime import date
from django.core.exceptions import ValidationError



@pytest.mark.django_db
def test_User():
    user = User.objects.create(username='test_user', email='test@example.com', password='testpassword',
                                    role='user')
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.role == 'user'

@pytest.mark.django_db
def test_travel_plans_creation1():
    admin_user = User.objects.create(username='admin_user', email='admin@example.com', password='adminpassword', role='admin')
    travel_plan = TravelPlans.objects.create(
        name='Test Plan',
        description='Test Description',
        price=100.0,
        start_date=date(2023, 8, 1),
        end_date=date(2023, 8, 5),
        registered_admin_id=admin_user.id
    )

    assert travel_plan.name == 'Test Plan'
    assert travel_plan.description == 'Test Description'
    assert travel_plan.price == 100.0
    assert travel_plan.start_date == date(2023, 8, 1)
    assert travel_plan.end_date == date(2023, 8, 5)
    assert travel_plan.registered_admin_id == admin_user.id

@pytest.mark.xfail
@pytest.mark.django_db
def test_travel_plan_invalid_dates(travel_plan_data):
    with pytest.raises(ValidationError) as exc_info:
        TravelPlans.objects.create(**travel_plan_data)
    assert "Invalid Dates!" in str(exc_info.value)

@pytest.mark.django_db
def test_registered_plan_creation(registered_plan_data):
    registered_plan = RegisteredPlans.objects.create(
        userID=registered_plan_data['user'],
        planID=registered_plan_data['travel_plan']
    )

    assert registered_plan.userID.username == 'test_user'
    assert registered_plan.planID.name == 'Test Plan'

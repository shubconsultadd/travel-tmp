from django.urls import path, include
from .views import *

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('login', UserLogin.as_view()),
    path('get_user_data', GetUserData.as_view()),
    path('add_plan', AddTravelPlans.as_view()),
    path('get_plans', GetAllTravelPlans.as_view()),
    path('get_plan/<int:plan_id>', GetTravelPlan.as_view()),
    path('delete_plan/<int:plan_id>/<int:admin_id>', DeleteTravelPlan.as_view(), name='delete-plan'),
    path('register_plan', RegisterForaPlan.as_view()),
    path('deregister/<int:userID>/<int:planID>', DeregisterFromAPlan.as_view(), name='de-register'),
    path('user_plans/<int:userID>', UserRegisteredPlans.as_view(), name='user-plans'),
    path('check_user_with_plan/<int:userID>/<int:planID>', IsUserRegisteredWithThePlan.as_view(), name='is-user'),
    path('modify_plan/<int:plan_id>', ModifyTravelPlans.as_view(),name='modify-plan'),
    path('plan_with_users/<int:planID>', ShowPlansWithRegisteredUsers.as_view(),name='show-plan'),
    path('get_admin_data/<int:adminID>', GetAdminUserName.as_view(),name='get-admin'),
]
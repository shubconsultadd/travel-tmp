import json

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.views import APIView
from rest_framework import status
# from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.utils.decorators import method_decorator
import requests
from .utils import *
from .decorators import user_check, is_user, is_admin, is_any_user

# Create your views here.

SPRING_BOOT_BASE_URL = "http://localhost:8080/api"


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(email=request.data.get('email')).first()

        dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
        }

        json_data = json.dumps(dict)
        return Response(dict, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        login_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'jwt': token
        }

        json_data = json.dumps(login_dict)

        response = HttpResponse(json_data, content_type='application/json', headers={
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Origin": "*"
        }, status=status.HTTP_201_CREATED)

        send_cookie(response=response, access_token=access_token, refresh_token=refresh_token)

        return response


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_any_user, 'dispatch')
class GetUserData(APIView):
    def get(self, request):
        token = request.headers["Authorization"].split("Bearer ")[1]
        print(token)
        decoded_token = jwt.decode(token, key='secret', algorithms=['HS256'])
        user_id = decoded_token.get('id')

        user = User.objects.filter(pk=user_id).first()

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        res = serializer.data
        res["id"] = user_id
        return Response(res, status=status.HTTP_200_OK)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_admin, 'dispatch')
class AddTravelPlans(APIView):

    def post(self, request):
        serializer = TravelPlansSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            result = serializer.data
            result["message"] = "Created Travel Plan"
            print(result)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_any_user, 'dispatch')
class GetAllTravelPlans(APIView):

    def get(self, request):
        travel_plans = TravelPlans.objects.all()
        serializer = TravelPlansSerializer(travel_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_any_user, 'dispatch')
class GetTravelPlan(APIView):
    def get(self, request, plan_id):
        travel_plan = TravelPlans.objects.filter(pk=plan_id).first()

        if travel_plan is None:
            return Response({"error": "Invalid Plan ID!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TravelPlansSerializer(travel_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_admin, 'dispatch')
class DeleteTravelPlan(APIView):

    def delete(self, request, plan_id, admin_id):
        travel_plan = TravelPlans.objects.get(pk=plan_id)

        if travel_plan is None:
            return Response({"error": "Travel plan not found"}, status=status.HTTP_404_NOT_FOUND)

        travel_plan.delete()
        return Response({"message": "Travel Plan Deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_user, 'dispatch')
class RegisterForaPlan(APIView):

    def post(self, request):

        user = User.objects.get(pk=request.data.get('userID'))

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        travel_plan = TravelPlans.objects.get(pk=request.data.get('planID'))

        if travel_plan is None:
            return Response({"error": "Travel plan not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegisteredPlansSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Travel plan registered with the user."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_user, 'dispatch')
class DeregisterFromAPlan(APIView):
    def delete(self, request, userID, planID):
        registered_plan = RegisteredPlans.objects.get(userID=userID, planID=planID)

        if registered_plan is None:
            return Response({"error": "Registered plan not found"}, status=status.HTTP_404_NOT_FOUND)

        registered_plan.delete()
        return Response({"success": "Successfully Deregistered from the plan."}, status=status.HTTP_204_NO_CONTENT)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_user, 'dispatch')
class UserRegisteredPlans(APIView):
    def get(self, request, userID):
        user = User.objects.get(pk=userID)

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        registered_plans = TravelPlans.objects.filter(registered_plans__pk=userID)

        serializer = TravelPlansSerializer(registered_plans, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_user, 'dispatch')
class IsUserRegisteredWithThePlan(APIView):
    def get(self, request, userID, planID):
        try:
            user = User.objects.get(pk=userID)

            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            plan = TravelPlans.objects.get(pk=planID)

            if plan is None:
                return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

            registered_plans = RegisteredPlans.objects.filter(userID=userID, planID=planID).exists()

            if registered_plans is True:
                return Response("true", status=status.HTTP_200_OK)

            else:
                return Response("false", status=status.HTTP_200_OK)


        except:
            return Response({"error": "Invalid userID or planID!"}, status=status.HTTP_404_NOT_FOUND)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_admin, 'dispatch')
class ModifyTravelPlans(APIView):
    def put(self, request, plan_id):
        travel_plan = TravelPlans.objects.get(pk=plan_id)

        if travel_plan is None:
            return Response({"error": "Travel Plan not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TravelPlansSerializer(travel_plan, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Updated the data!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(user_check, 'dispatch')
# @method_decorator(is_admin, 'dispatch')
class ShowPlansWithRegisteredUsers(APIView):
    def get(self, request, planID):
        plan = TravelPlans.objects.get(pk=planID)

        if plan is None:
            return Response({"error": "Travel Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        registered_users = User.objects.filter(registeredplans__planID=planID)

        serializer = UserSerializer(registered_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAdminUserName(APIView):
    def get(self, request, adminID):
        user = User.objects.filter(adminID).first()

        if user is None:
            return Response({"error": "Admin not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

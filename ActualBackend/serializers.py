import datetime
from datetime import datetime

from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TravelPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlans
        fields = "__all__"

    # def create(self, validated_data):
    #     instance = self.Meta.model(**validated_data)
    #     instance.save()
    #     return instance

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance

    def update(self, instance, validated_data):
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("Invalid Dates!")

        return data


class RegisteredPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredPlans
        fields = ['userID', 'planID']

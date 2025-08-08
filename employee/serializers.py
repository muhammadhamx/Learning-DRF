from rest_framework import serializers
from .models import User

class OwnerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            role='owner'
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user


class EmployeeCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        owner = self.context['request'].user
        employee = User(
            name=validated_data['name'],
            email=validated_data['email'],
            role='employee',
            owner=owner
        )
        employee.set_password(validated_data['password'])
        employee.save()
        return employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role']

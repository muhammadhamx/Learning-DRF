from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, AuthToken
from .serializers import UserSerializer, EmployeeCreateSerializer, OwnerRegisterSerializer
from rest_framework import status
from .decorators import token_auth_required, role_required

# Owner registeration
@api_view(['POST'])
def owner_register(request):
    serializer = OwnerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = AuthToken.objects.get_or_create(user=user)
        if created or not token.token:
            token.token = AuthToken.generate_token()
            token.save()

        return Response({'token': token.token, 'role': user.role}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        User.is_authenticated()
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    

# Create employee (owner only)
@api_view(['POST'])
@token_auth_required
@role_required(['owner'])
def employee_create(request):
    serializer = EmployeeCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Employee created successfully!"}, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List employees (owner only)
@api_view(['GET'])
@token_auth_required
@role_required(['owner'])
def list_employees(request):
    employees = request.user.employees.all()
    serializer = UserSerializer(employees, many=True)
    return Response(serializer.data)

# Profile (owner or employee both)
@api_view(['GET'])
@token_auth_required
@role_required(['owner', 'employee'])
def profile(request):
    user = request.user
    return Response({
        'name': user.name,
        'email': user.email,
        'role': user.role,
    })

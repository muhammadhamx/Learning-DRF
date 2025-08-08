from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,  mixins, permissions, generics
from .models import Author, Post, AuthToken
from .serializers import AuthorSerializer, AuthorWritableSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
import uuid
from employee.decorators import token_auth_required, role_required
from django.utils.decorators import method_decorator

# Create your views here.

'''
# Manual Control
class AuthorAPIView(APIView):
    def get(self, request):
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = AuthorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# GenericAPIView 
# (Handles GET List all and POST create new operations)
class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    


# Handles GET retrieve one, PUT/PATCH , DELETE.
class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# Automatic CRUD (ModelViewSet)
# combines all CRUD operations into one class.
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
'''

# Authentication View
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            author = Author.objects.get(email=email)
            if author.check_password(password):
                token = str(uuid.uuid4())  # Generate token
                AuthToken.objects.create(user=author, token=token)
                print('Login')
                return Response({"token": token, "role": author.role})
            return Response({"error": "Invalid password"}, status=400)
        except Author.DoesNotExist:
            return Response({"error": "Invalid email"}, status=400)

# Mixin Based CRUD
@method_decorator(token_auth_required, name='dispatch')
class AuthorListCreateView(mixins.ListModelMixin, 
                           mixins.CreateModelMixin, 
                           generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = AuthorWritableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
@method_decorator(token_auth_required, name='dispatch')
@method_decorator(role_required(['admin']), name='dispatch')
class AuthorDetailView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

'''
# For Nested Serializer
class AuthorWithPostsView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorWithPostsSerializer(authors, many=True)
        return Response(serializer.data)


# For Writable Nested Serializer
class AuthorCreateWithPostsView(APIView):
    def post(self, request):
        serializer = AuthorWritableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
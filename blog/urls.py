from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    #AuthorAPIView,
    AuthorListCreateView,
    AuthorDetailView,
    LoginView,
   # AuthorViewSet,
   # PostViewSet,
   # AuthorWithPostsView,
   # AuthorCreateWithPostsView
)
'''
# Router for ViewSets (Automatic CRUD)
router = DefaultRouter()
router.register('authors-viewset', AuthorViewSet, basename='authors-viewset')
router.register('posts-viewset', PostViewSet, basename='posts-viewset')
'''

urlpatterns = [
    
    # Manual APIView URLs
    #path('authors-api/', AuthorAPIView.as_view(), name='authors-api'),

    # GenericAPIView URLs
    #path('authors-generic/', AuthorListCreateView.as_view(), name='authors-generic'),
    #path('authors-generic/<uuid:pk>/', AuthorDetailView.as_view(), name='author-detail'),

    # Nested Serializer (Read-only)
    #path('authors-with-posts/', AuthorWithPostsView.as_view(), name='authors-with-posts'),

    # Writable Nested Serializer (Create author + posts)
    #path('create-author-with-posts/', AuthorCreateWithPostsView.as_view(), name='create-author-with-posts'),

    path('login/', LoginView.as_view(), name='login'),
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<uuid:pk>/', AuthorDetailView.as_view(), name='author-detail'),

]

# Add ViewSet routes automatically
#urlpatterns += router.urls

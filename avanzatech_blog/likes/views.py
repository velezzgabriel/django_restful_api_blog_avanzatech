from django.shortcuts import render

# Create your views here.

from .models import Like
from .serializers import LikeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView,  DestroyAPIView
from .pagination import LikePagination
from .filters import ListLikesFilterCustom
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Post
from django.shortcuts import get_object_or_404
from django.db.models import Q


class LikeCreate(CreateAPIView):

    pagination_class = LikePagination
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required for liking a post.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = LikeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['author'] != request.user.id:
            return Response({'error': 'Author must be the same as request.user.'}, status=status.HTTP_400_BAD_REQUEST)

        user_requester = self.request.user
        post_instance = Post.objects.get(pk=request.data["post_id"])
        permission = post_instance.permission

        if Like.objects.filter(post_id=request.data["post_id"], author=request.data["author"]).exists():
            return Response({'message': 'already liked'}, status=status.HTTP_204_NO_CONTENT)

        if user_requester.is_staff or permission in ['public', 'authenticated'] or (permission == 'team' and user_requester.team_id == post_instance.author.team_id) or user_requester.id == post_instance.author.id:
            return super().create(request, *args, **kwargs)

        return Response({'error': 'You dont comply with permissions needed to like a post.'}, status=status.HTTP_401_UNAUTHORIZED)


class LikeList(ListAPIView):

    pagination_class = LikePagination
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post_id', 'author']

    def get_queryset(self):

        queryset = Like.objects.all()

        user = self.request.user

        if user.is_anonymous:
            return queryset.filter(post_id__permission='public')

        elif user.is_authenticated and not user.is_staff:
            return queryset.filter(
                Q(post_id__permission__in=['public', 'authenticated']) |
                Q(post_id__permission='team', post_id__author__team_id=user.team_id) |
                Q(post_id__permission='author', post_id__author_id=user.id))

        elif user.is_staff:
            return queryset


class LikeDestroy(DestroyAPIView):
    pagination_class = LikePagination
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Like.objects.all()

    def get_queryset(self):
        user_requester = self.request.user
        post_id = self.kwargs['post_id']
        author_id = self.kwargs['author']

        if user_requester.is_staff or user_requester.id == author_id:
            return Like.objects.filter(post_id=post_id, author=author_id)

        if not author_id == user_requester.id:
            raise PermissionDenied('Users can only delete their own like')

        raise NotFound

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the post_id and author from the URL kwargs
        post_id = self.kwargs.get('post_id')
        author_id = self.kwargs.get('author')

        # Perform the lookup using post_id and author
        obj = queryset.filter(post_id=post_id, author=author_id).first()

        if obj is None:
            raise NotFound("No like found with the given post_id and author.")

        self.check_object_permissions(self.request, obj)
        return obj

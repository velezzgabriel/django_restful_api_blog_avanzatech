from django.shortcuts import render

# Create your views here.

from .models import Comment
from .pagination import CommentPagination
from .serializers import CommentSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from django.db.models import Q
from rest_framework.exceptions import NotFound, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend


class CommentCreate(CreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # filter_backends = (ListFilterCustom,)

    def get_queryset(self):
        return Comment.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required for commenting on a post.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['author'] != request.user.id:
            return Response({'error': 'Author commenting must be the same as request.user.'}, status=status.HTTP_400_BAD_REQUEST)

        user_requester = self.request.user
        post_instance = Post.objects.get(pk=request.data["post_id"])
        permission = post_instance.permission

# checking for view access to the post
        if user_requester.is_staff or permission in ['public', 'authenticated'] or (permission == 'team' and user_requester.team_id == post_instance.author.team_id) or user_requester.id == post_instance.author.id:
            return super().create(request, *args, **kwargs)

        return Response({'error': 'You dont comply with permissions needed to like a post.'}, status=status.HTTP_401_UNAUTHORIZED)


class CommentList(ListAPIView):

    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post_id', 'author']

    def get_queryset(self):

        queryset = Comment.objects.all()

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


class CommentDestroy(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.all()

    def get_queryset(self):
        user_requester = self.request.user
        comment_id = self.kwargs['pk']

        try:
            comment_instance = Comment.objects.get(pk=comment_id)
            comment_author = comment_instance.author
        except Comment.DoesNotExist:
            raise NotFound


# if the user is staff or the author of the comment
        if user_requester.is_staff or user_requester.id == comment_author.id:
            return Comment.objects.filter(pk=comment_id)

        if not comment_author == user_requester.id:
            raise PermissionDenied('Users can only delete their own like')

        raise NotFound

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the comment_id from the URL kwargs
        comment_id = self.kwargs['pk']

        # Perform the lookup using comment_id
        obj = queryset.filter(id=comment_id)

        if obj is None:
            raise NotFound("No comment found with the given pk.")

        self.check_object_permissions(self.request, obj)
        return obj

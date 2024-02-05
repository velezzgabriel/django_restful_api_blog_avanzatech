from .models import Post
from .serializers import PostSerializerCreateList, PostSerializerRetrieveUpdateDestroy

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS

from rest_framework.permissions import IsAuthenticated

from .pagination import PostPagination

from django_filters import rest_framework as filters

from .filters import ListFilterCustom

from django.shortcuts import get_object_or_404

# Create your views here.


# `/post` and `/post/<post_id>` list endpoint will only include posts the user has access to in the list and details endpoint will return a 404 if the user does not have view access to the post

class PostCreateOrList(ListCreateAPIView):

    pagination_class = PostPagination
    serializer_class = PostSerializerCreateList

    filter_backends = (ListFilterCustom,)

    def get_queryset(self):
        return Post.objects.all()

    def create(self, request, *args, **kwargs):
        # Check if the user is authenticated before allowing the creation of a new post
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required for creating a post.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Continue with the default create logic for authenticated users
        return super().create(request, *args, **kwargs)


class PostRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializerRetrieveUpdateDestroy
    pagination_class = PostPagination

    queryset = Post.objects.all()

    def get_queryset(self):
        user_requester = self.request.user
        post_instance = Post.objects.get(pk=self.kwargs['pk'])

        if self.request.method in SAFE_METHODS:

            if user_requester.is_staff:
                return Post.objects.filter(pk=self.kwargs['pk'])

            if user_requester.is_anonymous:
                return Post.objects.filter(permission='public')

            if post_instance.permission == 'team' and user_requester.team_id == post_instance.author.team_id:
                return Post.objects.filter(pk=self.kwargs['pk'])

            if post_instance.permission == 'authenticated' and user_requester.is_authenticated:
                return Post.objects.filter(pk=self.kwargs['pk'])

            if post_instance.permission == 'public' and user_requester.is_authenticated:
                return Post.objects.filter(pk=self.kwargs['pk'])

            if post_instance.permission == 'author' and user_requester.id == post_instance.author.id:
                return Post.objects.filter(pk=self.kwargs['pk'])

            raise NotFound

        else:

            if user_requester.is_staff or user_requester.id == post_instance.author.id:
                return Post.objects.filter(pk=self.kwargs['pk'])
            raise NotFound

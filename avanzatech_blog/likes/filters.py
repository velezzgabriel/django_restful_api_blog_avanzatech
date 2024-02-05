from rest_framework import filters
from .models import Like
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from posts.models import Post


class ListLikesFilterCustom(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_id = request.query_params.get('post_id')
        if post_id:
            post_instance = Post.objects.get(id=post_id)
            user = request.user
            permission = post_instance.permission

            if user.is_anonymous and permission == 'public':
                return queryset

            elif user.is_staff:
                return queryset

            elif user.is_authenticated:
                if permission == 'public' or permission == 'authenticated' or post_instance.author.id == user.id or post_instance.author.team_id == user.team_id:
                    return queryset

        # Default case: return an empty queryset
        return queryset.none()


# class ListLikesFilterCustom(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):

#         user = request.user
#         post_instance = Post.objects.get(id=self.kwargs['post_id'])
#         permission = post_instance.permission

#         if user.is_anonymous and permission == 'public':
#             return queryset

#         elif user.is_staff:
#             return queryset

#         elif user.is_authenticated:
#             if permission == 'public' or permission == 'authenticated' or post_instance.author.id == user.id or post_instance.author.team_id == user.team_id:
#                 return queryset

#         # Default case: return an empty queryset
#         return queryset.none()


class ListLikesFilterCustom(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        user = request.user

        if user.is_anonymous:
            return queryset.filter(post_id__permission='public')

        elif user.is_authenticated and not user.is_staff:
            return queryset.filter(
                Q(post_id__permission__in=['public', 'authenticated']) | Q(
                    author__id=user.id)
            ).union(
                queryset.filter(author__team_id=user.team_id,
                                post_id__permission__=['public', 'team', 'authenticated'])
            )

        elif user.is_staff:
            return queryset

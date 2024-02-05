from rest_framework import filters
from .models import Post
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404


class ListFilterCustom(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        user = request.user

        # If the user is anonymous, filter by 'public' permission
        if user.is_anonymous:
            return queryset.filter(permission='public')

        # If the user is authenticated and not an admin, apply additional filtering
        elif user.is_authenticated and not user.is_staff:
            return queryset.filter(
                Q(permission__in=['public', 'authenticated']) | Q(
                    author_id=user.id)
            ).union(
                queryset.filter(author__team_id=user.team_id)
            )

        # If the user is an admin, return all posts
        elif user.is_staff:
            return queryset

        # Default case: return an empty queryset
        return queryset.none()

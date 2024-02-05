from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post
from teams.models import Team
from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient
from .factories import PostFactory
from user.factories import CustomUserFactory, CustomUserSameTeamFactory
from teams.factories import TeamFactory
from user.models import CustomUser
from factory.django import DjangoModelFactory

#############   AUTHENTICATED USER TESTS  ################

# ______________________________________________________#


class PostAuthUserTestCreateListStandarAndBadRequests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

# ______________________________________________________#
    def test_list_post_by_auth_user_(self):
        url = reverse('postCreateOrList')
# auth permission posts
        PostFactory.create_batch(19, permission='authenticated')
# public posts
        for _ in range(20):
            PostFactory(permission='public')
# 6 different users from the same team
        users_same_team = [CustomUserFactory(
            team_id=self.team) for _ in range(21)]
    # 6xUsers post 6xPosts with permission: 'team'
        for user in users_same_team:
            PostFactory(permission='team', author=user)
# request.user doing 5 posts
        for _ in range(22):
            PostFactory(permission='author', author=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data.get("results")), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 82)
        self.assertEqual(Post.objects.all().count(), 82)
        self.assertEqual(CustomUser.objects.all().count(), 61)


# ______________________________________________________#

    def test_create_post_by_authenticated_user(self):
        url = reverse('postCreateOrList')
        data = {
            "id": 1,
            "title": 'test_create_post',
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'test_create_post')
        # self.assertEqual(data, response.data)

# ______________________________________________________#
    def test_create_post_None_title(self):
        url = reverse('postCreateOrList')
        data = {
            "title": None,
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_None_post_content(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": None,
            "permission": 'author',
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_None_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": None,
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_None_author(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "authenticated",
            "author": None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_blank_title(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "",
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_blank_post_content(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "",
            "permission": 'author',
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_blank_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "",
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# ______________________________________________________#
    def test_create_post_blank_author(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "authenticated",
            "author": "",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

        self.assertEqual(response.data.get('detail'),
                         None)

# ______________________________________________________#
    def test_create_post_wrong_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "non existent",
            "author": self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.data.get('detail'),
                         None)

# ______________________________________________________#


class PostAuthUserTestIdeal(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

# ______________________________________________________#
    def test_list_post_by_authenticated_user_not_author_not_admin(self):
        url = reverse('postCreateOrList')

        PostFactory.create_batch(10, permission='authenticated')

        users_same_team = [CustomUserFactory(
            team_id=self.team) for _ in range(6)]

        for _ in range(7):
            PostFactory(permission='public')

        for user in users_same_team:
            PostFactory(permission='team', author=user)

        for _ in range(5):
            PostFactory(permission='author', author=self.user)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 28)
        self.assertEqual(Post.objects.all().count(), 28)
        self.assertEqual(CustomUser.objects.all().count(), 24)


# ______________________________________________________#

class PostAuthUserListTest(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

# ______________________________________________________#
    def test_list_post_by_auth_user_return_all(self):
        url = reverse('postCreateOrList')
# auth permission posts
        PostFactory.create_batch(10, permission='authenticated')
# public posts
        for _ in range(7):
            PostFactory(permission='public')
# 6 different users from the same team
        users_same_team = [CustomUserFactory(
            team_id=self.team) for _ in range(6)]
    # 6xUsers post 6xPosts with permission: 'team'
        for user in users_same_team:
            PostFactory(permission='team', author=user)
# request.user doing 5 posts
        for _ in range(5):
            PostFactory(permission='author', author=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 28)
        self.assertEqual(Post.objects.all().count(), 28)
        self.assertEqual(CustomUser.objects.all().count(), 24)

# ______________________________________________________#
    def test_list_post_by_auth_user_in_unique_team(self):
        url = reverse('postCreateOrList')
# authenticated posts
        PostFactory.create_batch(10, permission='authenticated')
# public posts
        for _ in range(7):
            PostFactory(permission='public')
# team posts. doesnt add to response
        for _ in range(6):
            PostFactory(permission='team')
# author posts
        for _ in range(5):
            PostFactory(permission='author', author=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 22)
        self.assertEqual(Post.objects.all().count(), 28)
        self.assertEqual(CustomUser.objects.all().count(), 24)

# ______________________________________________________#
    def test_list_post_by_auth_user_in_unique_team_no_author(self):
        url = reverse('postCreateOrList')
# authenticated posts
        PostFactory.create_batch(10, permission='authenticated')
# public posts
        for _ in range(7):
            PostFactory(permission='public')
# team posts. doesnt add to response
        for _ in range(6):
            PostFactory(permission='team')
# author posts
        for _ in range(5):
            PostFactory(permission='author')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)
        self.assertEqual(Post.objects.all().count(), 28)
        self.assertEqual(CustomUser.objects.all().count(), 29)

# ______________________________________________________#
    def test_list_post_by_auth_user_only_author(self):
        url = reverse('postCreateOrList')
# team posts. doesnt add to response
        for _ in range(6):
            PostFactory(permission='team')
# author posts
        for _ in range(5):
            PostFactory(permission='author', author=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.all().count(), 11)
        self.assertEqual(CustomUser.objects.all().count(), 7)


# ______________________________________________________#


class PostAuthUserRetrieve(APITestCase):

    def setUp(self):
        self.team = TeamFactory(team_name='requester team')
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)


# ______________________________________________________#


    def test_post_auth_user_retrieve_permission_authenticated(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_auth_user_retrieve_permission_public(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_auth_user_retrieve_permission_team_requester_from_same_team(self):

        self.user_sameteam = CustomUserFactory(team_id=self.team)

        self.post = PostFactory(permission='team', author=self.user_sameteam)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_auth_user_fails_to_retrieve_different_team_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#

    def test_post_auth_user_fails_to_retrieve_different_author_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_auth_user_retrieves_same_author_post(self):

        self.post = PostFactory(permission='author', author=self.user)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)


#############   ADMIN USER TESTS  ################

# ______________________________________________________#
class PostAdminUserListCreateTests(APITestCase):

    def setUp(self):
        self.admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(user=self.admin_user)

        self.team = TeamFactory(team_name='requester team')

# # ______________________________________________________#
    def test_list_publicpost_by_admin(self):

        url = reverse('postCreateOrList')

# public posts
        for _ in range(4):
            PostFactory(permission='public')

        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data.get("results")), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(Post.objects.all().count(), 4)
        self.assertEqual(CustomUser.objects.all().count(), 5)

# # ______________________________________________________#
    def test_list_authpost_by_admin(self):

        url = reverse('postCreateOrList')

        PostFactory.create_batch(4, permission='authenticated')

        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data.get("results")), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(Post.objects.all().count(), 4)
        self.assertEqual(CustomUser.objects.all().count(), 5)

# # ______________________________________________________#
    def test_list_teampost_by_admin(self):

        url = reverse('postCreateOrList')

        for user in range(4):
            PostFactory(permission='team')

        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data.get("results")), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(Post.objects.all().count(), 4)
        self.assertEqual(CustomUser.objects.all().count(), 5)

# # ______________________________________________________#
    def test_list_authorpost_by_admin(self):

        url = reverse('postCreateOrList')

        for _ in range(4):
            PostFactory(permission='author')

        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data.get("results")), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(Post.objects.all().count(), 4)
        self.assertEqual(CustomUser.objects.all().count(), 5)

# # ______________________________________________________#
    def test_create_post_by_admin_user(self):
        url = reverse('postCreateOrList')
        data = {
            "id": 1,
            "title": 'test_create_post',
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'test_create_post')

# # ______________________________________________________#
    def test_create_post_None_title_byadmin(self):
        url = reverse('postCreateOrList')
        data = {
            "title": None,
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_None_post_content(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": None,
            "permission": 'author',
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_None_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": None,
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_None_author(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "authenticated",
            "author": None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_blank_title(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "",
            "post_content": 'test_content__',
            "permission": 'author',
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_blank_post_content(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "",
            "permission": 'author',
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_blank_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "",
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

# # ______________________________________________________#
    def test_create_post_blank_author(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "authenticated",
            "author": "",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

        self.assertEqual(response.data.get('detail'),
                         None)

# # ______________________________________________________#
    def test_create_post_wrong_permission(self):
        url = reverse('postCreateOrList')
        data = {
            "title": "test_title",
            "post_content": "test_content",
            "permission": "non existent",
            "author": self.admin_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.data.get('detail'),
                         None)

# ______________________________________________________#


class PostAdminUserRetrieve(APITestCase):

    def setUp(self):
        self.admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(user=self.admin_user)

        self.team = TeamFactory(team_name='requester team')

# ______________________________________________________#

    def test_post_admin_user_retrieve_permission_authenticated(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_admin_user_retrieve_permission_public(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_admin_user_retrieve_permission_team_requester_from_same_team(self):

        self.user_sameteam = CustomUserFactory(team_id=self.team)

        self.post = PostFactory(permission='team', author=self.user_sameteam)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_admin_user_retrieves_different_team_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#

    def test_post_admin_user_retrieves_different_author_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#
    def test_post_admin_user_retrieves_same_author_post(self):

        self.post = PostFactory(permission='author', author=self.admin_user)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

# ______________________________________________________#


class PostAdminUserUpdate(APITestCase):

    def setUp(self):
        self.admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(user=self.admin_user)

        self.team = TeamFactory(team_name='requester team')
        # self.user = CustomUserFactory(team_id=self.team)
        # self.client.force_authenticate(user=self.user)

# ______________________________________________________#

    def test_post_admin_user_updates_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_updates_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_updates_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_updates_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#

    def test_post_admin_user_updates_same_author_post(self):

        self.post = PostFactory(permission='author', author=self.admin_user)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.get(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

# ______________________________________________________#


class PostAdminUserPatch(APITestCase):

    def setUp(self):
        self.admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(user=self.admin_user)

        self.team = TeamFactory(team_name='requester team')
        # self.user = CustomUserFactory(team_id=self.team)
        # self.client.force_authenticate(user=self.user)

# ______________________________________________________#

    def test_post_admin_user_patch_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_patch_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_patch_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    # ______________________________________________________#

    def test_post_admin_user_patch_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 2)

# ______________________________________________________#

    def test_post_admin_user_patch_same_author_post(self):

        self.post = PostFactory(permission='author', author=self.admin_user)

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)


# ______________________________________________________#

class PostAuthUserUpdate(APITestCase):
    pass

# ______________________________________________________#


class PostAuthUserDelete(APITestCase):
    pass


#############   NON AUTHENTICATED USER TESTS  ################

class PostNonAuthUserListCreate(APITestCase):

    def test_create_post_by_non_auth_user(self):
        url = reverse('postCreateOrList')
        data = {
            "title": 'test_create_post',
            "post_content": 'test_content__',
            "permission": 'author',
            "author": None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.data.get('detail'),
                         None)
        self.assertEqual(response.data.get('error'),
                         'Authentication required for creating a post.')

# ______________________________________________________#
    def test_list_post_by_non_auth_user_public(self):
        url = reverse('postCreateOrList')

        PostFactory.create_batch(10, permission='authenticated')

        for _ in range(11):
            PostFactory(permission='public')
        for _ in range(6):
            PostFactory(permission='authenticated')
        for _ in range(7):
            PostFactory(permission='team')
        for _ in range(8):
            PostFactory(permission='author')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
# ______________________________________________________#


class PostNonAuthUserRetrieve(APITestCase):

    def setUp(self):

        self.team = TeamFactory(team_name='requester team')

    # ______________________________________________________#

    def test_post_non_auth_user_retrieves_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

# ______________________________________________________#


class PostNonAuthUserUpdatePut(APITestCase):

    def setUp(self):

        self.team = TeamFactory(team_name='requester team')

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_update_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_update_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_update_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_update_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

# ______________________________________________________#


class PostNonAuthUserPatch(APITestCase):

    def setUp(self):

        self.team = TeamFactory(team_name='requester team')

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_patch_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'post_content': 'updated content',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_patch_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'post_content': 'updated content',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_patch_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_patch_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        updated_data = {
            'title': 'Updated Title',
            'permission': 'author',
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

# ______________________________________________________#


class PostNonAuthUserDelete(APITestCase):

    def setUp(self):

        self.team = TeamFactory(team_name='requester team')

    # ______________________________________________________#

    def test_post_non_auth_user_retrieves_publicPermission_post(self):

        self.post = PostFactory(permission='public')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_authenticatedPermission_post(self):

        self.post = PostFactory(permission='authenticated')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_teamPermission_post(self):

        self.post = PostFactory(permission='team')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

    # ______________________________________________________#

    def test_post_non_auth_user_fails_to_retrieve_authorPermission_post(self):

        self.post = PostFactory(permission='author')

        url = reverse('postRetrieveUpdateDestroy', kwargs={'pk': self.post.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all().count(), 1)

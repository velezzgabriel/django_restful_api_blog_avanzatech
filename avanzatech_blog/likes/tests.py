from django.test import TestCase

# Create your tests here.

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from factory.django import DjangoModelFactory

from .models import Like
from .factories import LikeFactory

from posts.models import Post
from posts.factories import PostFactory

from teams.models import Team
from teams.factories import TeamFactory

from user.models import CustomUser
from user.factories import CustomUserFactory


#####################   CREATE LIKES TESTS  #####################

# ----------------   AUTHENTICATED USER TESTS  ----------------#
class LikesCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

    def test_auth_user_likes_public_post(self):
        post = PostFactory(permission='public')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_auth_user_likes_authenticatedpermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_auth_user_likes_sameteam_teampermission_post(self):
        post = PostFactory(permission='team', author__team_id=self.team)

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_auth_user_likes_own_post(self):
        post = PostFactory(permission='team', author=self.user)

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_auth_user_FAILS_to_like_differentteam_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_auth_user_FAILS_to_like_differentauthor_permission_post(self):
        post = PostFactory(permission='author')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_auth_user_FAILS_to_like_non_existing_post(self):
        post = PostFactory(permission='authorized')

        url = reverse('likesCreate')
        data = {
            "post_id": 100,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_auth_user_FAILS_to_like_because_postid_is_not_in_payload(self):
        post = PostFactory(permission='team')

        url = reverse('likesCreate')
        data = {
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_auth_user_FAILS_to_like_because_author_is_not_in_payload(self):
        post = PostFactory(permission='team')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_auth_user_FAILS_to_like_an_already_liked_post(self):
        post = PostFactory(permission='team')
        LikeFactory(post_id=post, author=self.user)

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)


# ----------------   NON AUTHENTICATED USER TESTS  ----------------#
class LikesNonAuthUserCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_FAILS_to_like_publicpermission_post(self):
        post = PostFactory(permission='public')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_NON_auth_user_FAILS_to_like_authenticatedpermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_NON_auth_user_FAILS_to_like_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)

    def test_NON_auth_user_FAILS_to_like_authorpermission_post(self):
        post = PostFactory(permission='author')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)


# ----------------   ADMIN USER TESTS  ----------------#
class LikesAdminUserCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_likes_publicpermission_post(self):
        post = PostFactory(permission='public')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_admin_user_likes_teampermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_admin_user_likes_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_admin_user_likes_differentauthor_authorpermission_post(self):
        other_author = CustomUserFactory()
        post = PostFactory(permission='author', author=other_author)

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_admin_user_likes_own_authorpermission_post(self):
        post = PostFactory(permission='author')

        url = reverse('likesCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)


#####################   LIST LIKES TESTS  #####################

# ----------------   AUTHENTICATED USER TESTS  ----------------#

class LikesAuthenticatedListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

    def test_auth_user_lists_public_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='public')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_authenticatedpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='authenticated')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_sameteam_teampermission_post(self):
        post = PostFactory(permission='team', author__team_id=self.team)
        for _ in range(5):
            LikeFactory(post_id=post, author__team_id=self.team)

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 7)

    def test_auth_user_lists_differentteam_teampermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='team')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_own_likes_from_own_post(self):

        for _ in range(5):
            LikeFactory(post_id__permission='team',
                        author=self.user, post_id__author=self.user)

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_auth_user_FAILS_to_list_differentauthor_permission_post(self):

        random_user = CustomUserFactory()

        for _ in range(5):
            LikeFactory(post_id__permission='author',
                        post_id__author=random_user,
                        author=random_user)

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   NON AUTHENTICATED USER TESTS  ----------------#


class LikesNonAuthenticatedListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_lists_publicpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='public')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_lists_authenticatedpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='authenticated')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_list_teampermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='team')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_list_authorpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='author')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)


# ----------------   ADMIN USER TESTS  ----------------#
class LikesAdminListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_lists_publicpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='public')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_authenticatedpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='authenticated')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_teampermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='team')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_differentauthor_authorpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='author')

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_own_authorpermission_post(self):
        for _ in range(5):
            LikeFactory(post_id__permission='author',
                        post_id__author=self.user)

        url = reverse('likesList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 6)


#####################   DESTROY LIKES TESTS  #####################

class LikesDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

# ______________________________________________________#

# ----------------   AUTHENTICATED USER TESTS  ----------------#

    def test_auth_user_FAILS_to_destroy_anotherowner_like(self):
        like = LikeFactory(post_id__permission='public')
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_auth_user_destroys_own_like(self):
        like = LikeFactory(author=self.user)
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   NON AUTHENTICATED USER TESTS  ---------------#
class LikesNonAuthDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_FAILS_to_destroy_a_like_of_a_publicpermission_post(self):
        # Set up a Post with 'public' permission, a Like, and a non-authenticated User
        post = PostFactory(permission='public')
        user = CustomUserFactory()
        like = LikeFactory(post_id=post, author=user)

        # Attempt to delete the Like as the non-authenticated User
        # Ensure the client is not authenticated
        # self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse('likesDestroy', kwargs={'post_id': post.id, 'author': user.id}))

        # Check that the deletion was not successful
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertTrue(Like.objects.filter(pk=like.pk).exists())


# ----------------   ADMIN USER TESTS  ----------------#
class LikesAdminDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_destroys_differentowner_like_in_differentowner_publicpermission_post(self):
        like = LikeFactory(post_id__permission='public')
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_like_in_differentowner_authenticatedpermission_post(self):
        like = LikeFactory(post_id__permission='authenticated')
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_like_in_differentowner_teampermission_post(self):
        like = LikeFactory(post_id__permission='team')
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_like_in_differentowner_authorpermission_post(self):
        like = LikeFactory(post_id__permission='author')
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_like_in_own_authorpermission_post(self):
        like = LikeFactory(post_id__permission='author',
                           post_id__author=self.user)
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_destroys_own_like_in_own_authorpermission_post(self):
        like = LikeFactory(post_id__permission='author', author=self.user)
        post = like.post_id
        author = like.author

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_FAILS_to_destroy_a_non_existing_like(self):
        post = PostFactory()
        author = CustomUserFactory()

        url = reverse('likesDestroy', kwargs={
                      'post_id': post.id, 'author': author.id})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

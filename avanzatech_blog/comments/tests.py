from django.test import TestCase

# Create your tests here.

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from factory.django import DjangoModelFactory

from .models import Comment
from .factories import CommentFactory

from posts.models import Post
from posts.factories import PostFactory

from teams.models import Team
from teams.factories import TeamFactory

from user.models import CustomUser
from user.factories import CustomUserFactory


#####################   CREATE COMMENT TESTS  #####################

# ----------------   AUTHENTICATED USER TESTS  ----------------#
class CommentsCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

    def test_auth_user_comments_not_owned_public_post(self):
        post = PostFactory(permission='public')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_comments_not_owned_authenticatedpermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_comments_sameteam_not_ownedteampermission_post(self):
        post = PostFactory(permission='team', author__team_id=self.team)

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_comments_own_post(self):
        post = PostFactory(permission='author', author=self.user)

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_auth_user_FAILS_to_comment_differentteam_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('commentsCreate')
        data = {

            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"

        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_FAILS_to_comment_differentauthor_authorpermission_post(self):
        post = PostFactory(permission='author')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_FAILS_to_comment_non_existing_post(self):
        post = PostFactory(permission='authorized')

        url = reverse('commentsCreate')
        data = {

            "post_id": 100,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_FAILS_to_comment_because_postid_is_not_in_payload(self):
        post = PostFactory(permission='team')

        url = reverse('commentsCreate')
        data = {
            "author": self.user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_FAILS_to_comment_because_author_is_not_in_payload(self):
        post = PostFactory(permission='team')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_comments_fourtimes_in_a_post(self):
        post = PostFactory(permission='authenticated')
        # LikeFactory(post_id=post, author=self.user)

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"

        }

        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   NON AUTHENTICATED USER TESTS  ----------------#
class CommentsNonAuthUserCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_FAILS_to_comment_publicpermission_post(self):
        post = PostFactory(permission='public')

        url = reverse('commentsCreate')
        data = {

            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_NON_auth_user_FAILS_to_comment_authenticatedpermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('commentsCreate')
        data = {

            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_NON_auth_user_FAILS_to_comment_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_NON_auth_user_FAILS_to_comment_authorpermission_post(self):
        post = PostFactory(permission='author')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   ADMIN USER TESTS  ----------------#
class CommentsAdminUserCreateTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_comments_publicpermission_post(self):
        post = PostFactory(permission='public')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_comments_authenticatedpermission_post(self):
        post = PostFactory(permission='authenticated')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_comments_differentteam_teampermission_post(self):
        post = PostFactory(permission='team')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_comments_differentauthor_authorpermission_post(self):
        other_author = CustomUserFactory()
        post = PostFactory(permission='author', author=other_author)

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_comments_own_authorpermission_post(self):
        post = PostFactory(permission='author')

        url = reverse('commentsCreate')
        data = {
            "post_id": post.id,
            "author": self.user.id,
            "comment_content": "This is a comment"

        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 2)


#####################   LIST COMMENT TESTS  #####################

# ----------------   AUTHENTICATED USER TESTS  ----------------#

class CommentsAuthenticatedListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)

    def test_auth_user_lists_comments_from_public_post(self):

        for _ in range(5):
            CommentFactory(post_id__permission='public')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_comments_from_authenticatedpermission_posts(self):
        for _ in range(5):
            CommentFactory(post_id__permission='authenticated')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.data['count'], 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_all_comments_from_the_same_authenticatedpermission_posts(self):
        # create 5 comments from the same post
        post = PostFactory(permission='authenticated')

        for _ in range(5):
            CommentFactory(post_id=post, author=self.user)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_auth_user_lists_likes_from_two_posts_of_sameteamauthors_teampermission_post(self):
        post = PostFactory(permission='team', author__team_id=self.team)
        for _ in range(5):
            CommentFactory(post_id=post, author__team_id=self.team)

        post = PostFactory(permission='team', author__team_id=self.team)
        for _ in range(5):
            CommentFactory(post_id=post, author__team_id=self.team)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 10)
        self.assertEqual(CustomUser.objects.count(), 13)

    def test_auth_user_lists_differentteam_teampermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='team',
                           author__team_id=self.team, post_id__author__team_id=self.team)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_auth_user_lists_own_comments_from_own_post(self):

        for _ in range(5):
            CommentFactory(post_id__permission='team',
                           author=self.user, post_id__author=self.user)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_auth_user_FAILS_to_list_differentauthor_authorpermission_post(self):

        random_user = CustomUserFactory()

        for _ in range(5):
            CommentFactory(post_id__permission='author',
                           post_id__author=random_user,
                           author=random_user)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   NON AUTHENTICATED USER TESTS  ----------------#


class CommentsNonAuthenticatedListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_lists_comments_of_publicpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='public')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_lists_comments_of_authenticatedpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='authenticated')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_list_comments_of_teampermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='team')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_NON_auth_user_FAILS_to_list_authorpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='author')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)


# ----------------   ADMIN USER TESTS  ----------------#
class CommentsAdminListTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_lists_comments_of_publicpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='public')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_comments_of_authenticatedpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='authenticated')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_comments_of_teampermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='team')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_comments_of_differentauthor_authorpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='author')

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 11)

    def test_admin_user_lists_comments_of_own_authorpermission_post(self):
        for _ in range(5):
            CommentFactory(post_id__permission='author',
                           post_id__author=self.user)

        url = reverse('commentsList')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 6)


#####################   DESTROY COMMENT TESTS  #####################

class CommentsAuthUserDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)
        self.client.force_authenticate(user=self.user)


# ----------------   AUTHENTICATED USER TESTS  ----------------#


    def test_auth_user_FAILS_to_destroy_anotherowner_comment(self):
        comment = CommentFactory(post_id__permission='public')

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={
                      'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_auth_user_destroys_own_comment(self):
        comment = CommentFactory(author=self.user)

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={
                      'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)


# ----------------   NON AUTHENTICATED USER TESTS  ---------------#
class CommentsNonAuthDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team)

    def test_NON_auth_user_FAILS_to_destroy_a_comment_of_a_publicpermission_post(self):
        comment = CommentFactory(post_id__permission='public')

        pk = comment.id

        response = self.client.delete(
            reverse('commentsDestroy', kwargs={'pk': pk}))

        # Check that the deletion was not successful
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(pk=pk).exists())
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_NON_auth_user_FAILS_to_destroy_a_comment_of_a_authenticatedpermission_post(self):
        comment = CommentFactory(post_id__permission='authenticated')

        pk = comment.id

        response = self.client.delete(
            reverse('commentsDestroy', kwargs={'pk': pk}))

        # Check that the deletion was not successful
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(pk=pk).exists())
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_NON_auth_user_FAILS_to_destroy_a_comment_of_a_authorpermission_post(self):
        comment = CommentFactory(post_id__permission='author')

        pk = comment.id

        response = self.client.delete(
            reverse('commentsDestroy', kwargs={'pk': pk}))

        # Check that the deletion was not successful
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(pk=pk).exists())
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 3)


# ----------------   ADMIN USER TESTS  ----------------#
class CommentsAdminDestroyTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team_id=self.team, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_admin_user_destroys_differentowner_comments_in_differentowner_publicpermission_post(self):
        comment = CommentFactory(post_id__permission='public')

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_comments_in_differentowner_authenticatedpermission_post(self):
        comment = CommentFactory(post_id__permission='authenticated')

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_comments_in_differentowner_teampermission_post(self):
        comment = CommentFactory(post_id__permission='team')

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_comments_in_differentowner_authorpermission_post(self):
        comment = CommentFactory(post_id__permission='author')

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_admin_user_destroys_differentowner_comments_in_own_authorpermission_post(self):
        comment = CommentFactory(post_id__permission='author',
                                 post_id__author=self.user)

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_destroys_own_comments_in_own_authorpermission_post(self):
        comment = CommentFactory(
            post_id__permission='author', author=self.user)

        pk = comment.id

        url = reverse('commentsDestroy', kwargs={'pk': pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_user_FAILS_to_destroy_a_non_existing_comments(self):
        post = PostFactory()
        author = CustomUserFactory()

        url = reverse('commentsDestroy', kwargs={'pk': 100})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 3)

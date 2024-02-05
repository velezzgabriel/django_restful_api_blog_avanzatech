from django.urls import path

from .views import LikeCreate, LikeList, LikeDestroy


urlpatterns = [
    path('create/', LikeCreate.as_view(), name='likesCreate'),
    path('', LikeList.as_view(), name='likesList'),
    path('<int:author>/<int:post_id>/',
         LikeDestroy.as_view(), name='likesDestroy'),
]

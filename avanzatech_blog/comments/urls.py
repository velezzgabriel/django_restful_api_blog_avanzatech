from django.urls import path

from .views import CommentCreate, CommentList, CommentDestroy


urlpatterns = [
    path('', CommentCreate.as_view(), name='commentsCreate'),
    path('list/', CommentList.as_view(), name='commentsList'),
    path('<int:pk>/', CommentDestroy.as_view(),
         name='commentsDestroy'),

]

from django.urls import path

from posts.views import PostCreateOrList, PostRetrieveUpdateDestroy


urlpatterns = [
    path('', PostCreateOrList.as_view(), name='postCreateOrList'),
    path('<int:pk>/', PostRetrieveUpdateDestroy.as_view(),
         name='postRetrieveUpdateDestroy'),

]

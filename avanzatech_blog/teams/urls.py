from django.urls import path

from teams.views import TeamCreateOrList, TeamRetrieveUpdateDestroy


# urlpatterns = [
#     path('', TeamCreateOrList.as_view(), name='teamsCreateOrList'),
#     path('<int:pk>/', TeamRetrieveUpdateDestroy.as_view(),
#          name='teamsRetrieveUpdateDestroy'),

# ]

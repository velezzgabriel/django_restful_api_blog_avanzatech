from django.shortcuts import render


from .models import Team
from .serializers import TeamSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.


# class TeamCreateOrList(ListCreateAPIView):

#     def post(self, request):
#         serializer = TeamSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         posts = Team.objects.all()
#         serializer = TeamSerializer(posts, many=True)
#         return Response(serializer.data)


# class TeamRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
#     serializer_class = TeamSerializer
#     queryset = Team.objects.all()

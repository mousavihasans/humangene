from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from customersupport.models import TrackTask
from customersupport.serializers import TrackTasksSerializer


class TaskList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrackTasksSerializer

    def get_queryset(self):
        return TrackTask.objects.filter(user=self.request.user)

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from accounts.models import OrganizerUser
from .models import Diary
from .forms import DiaryForm
from .serializers import DiaryListSerializer, DiarySerializer


class DiaryItemView(RetrieveAPIView):
    queryset = Diary.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DiarySerializer
    lookup_field = 'title'


class DiaryListViewSet(ListCreateAPIView):
    queryset = Diary.objects.all()          ## TODO: order_by(owner)
    permission_classes = (AllowAny,)
    serializer_class = DiaryListSerializer
    lookup_field = 'title'

    def post(self, request):
        get_owner = request.data['owner']
        get_title = request.data['title']
        get_body = request.data['body']
        try:
            user = OrganizerUser.objects.get(pk=get_owner)
            diary_item = Diary.objects.create(owner=user, title=get_title, body=get_body)
            serialized_data = self.get_serializer(diary_item)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
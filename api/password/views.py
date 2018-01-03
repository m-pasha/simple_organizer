from django.conf import settings
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from accounts.models import OrganizerUser
from .serializers import PasswordOrganizerListSerializer, PasswordOrganizerSerializer
from .models import PasswordOrganizer


class PasswordOrganizerItemView(RetrieveAPIView):
    queryset = PasswordOrganizer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordOrganizerSerializer
    lookup_field = 'pk'


class PasswordOrganizerListViewSet(ListCreateAPIView):
    queryset = PasswordOrganizer.objects.all()          ## TODO: order_by(owner)
    permission_classes = (AllowAny,)
    serializer_class = PasswordOrganizerListSerializer

    def post(self, request):
        get_owner = request.data['owner']
        get_resource_url = request.data['resource_url']
        get_password_res = request.data['password_res']

        try:
            user = OrganizerUser.objects.get(pk=get_owner)
            passwordorganizer_item = PasswordOrganizer.objects.create(owner=user, resource_url=get_resource_url,
                                                                      password_res=get_password_res)
            serialized_data =self.get_serializer(passwordorganizer_item)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# def passorg(request):
#     if request.user.is_authenticated():
#         return render (request, 'passorg.html', {'pass_list': PasswordOrganizer.objects.all().filter(
#             owner=request.user), 'user_avatar': request.user.main_menu_avatar})
#     else:
#         return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
#
#
# def create_passw(request):
#     if request.user.is_authenticated():
#         if request.method == 'POST':
#             form = PasswordOrganizerForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('/passorg/all/')
#         else: # ==>GET method
#             return render(request, 'create_passw.html', {'form': PasswordOrganizerForm})
#     else:
#         return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from .models import OrganizerUser
from .serializers import OrganizerUserListSerializer, OrganizerUserSerializer


class OrganizerUserItemView(RetrieveAPIView):
    queryset = OrganizerUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrganizerUserSerializer
    lookup_field = 'user_mail'


class OrganizerUserViewSet(ListCreateAPIView):
    queryset = OrganizerUser.objects.all()          # TODO: order_by(owner)
    permission_classes = (AllowAny,)
    serializer_class = OrganizerUserListSerializer
    # lookup_field = 'user_mail'

    def post(self, request):
        get_user_mail = request.data['user_mail']
        # get_first_name = request.data['first_name']
        # get_second_name = request.data['second_name']
        get_password = request.data['password']
        try:
            organizer_user_item = OrganizerUser.objects.create_user(user_mail=get_user_mail, password=get_password)
            serialized_data = self.get_serializer(organizer_user_item)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)

            # logger.info("User with e-mail# %s. Successfully created" % request.data.get("email"))
            #     return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
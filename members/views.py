from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import send_mail
from humangene import settings
from members.models import Member
from members.serializers import RegisterSerializer, VerifySerializer, MemberSerializer, IncreaseCreditViaBankSerializer


class RegisterView(APIView):
    def post(self, request):
        
        # register_manager = RegisterManager()
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # todo: make atomic

        member, _ = Member.objects.get_or_create(email=serializer.data['email'],
                                                 password=serializer.data['password'],
                                                 defaults=dict(
                                                    is_active=True,
                                                 ))

        result = {
            'success': True,
            }

        return Response(result)


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.member = Member.objects.get(email=serializer.data['email'], password=serializer.data['password'])
        except Exception as e:
            raise ValidationError('Email or password is wrong!.')
        serialized_member = MemberSerializer(serializer.member).data
        serialized_member['token'] = Token.objects.get(user=self.member).key

        return Response(serialized_member)


class UserProfileView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """
    Returns Member's details in JSON format.
    """
    serializer_class = MemberSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return Member.objects.get(pk=self.request.user.pk)


class TransactionListView(ListModelMixin, GenericAPIView):
    serializer_class = IncreaseCreditViaBankSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

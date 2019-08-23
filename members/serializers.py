from django.core import exceptions
from rest_framework import serializers

import django.contrib.auth.password_validation as validators

from humangene import settings
from members.models import Member, IncreaseCreditViaBank


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=50)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = Member(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=Member)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterSerializer, self).validate(data)


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=50)

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            self.member = Member.objects.get(email=email, password=password)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Member {} for {} does not exist".format(email, password))

        return data

    def save(self):
        self.member.is_active = True
        self.member.save()


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'credit', 'profile_picture')
        read_only_fields = ('email', 'credit')


class IncreaseCreditViaBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncreaseCreditViaBank
        fields = ('id', 'amount', 'status', 'tracking_code', 'created_at')
        read_only_fields = ('id', 'amount', 'status', 'tracking_code', 'created_at')

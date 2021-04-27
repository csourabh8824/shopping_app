from rest_framework import serializers
from django.contrib.auth import authenticate
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import RegisterSerializer
from .models import UserProfile, Address

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False    )
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)

    class Meta:
        model = UserProfile
        fields = ["id", "username", "email", "password", "first_name", "last_name",
                  "mobile_number", "alternate_mobile_number", "gender", "birthdate"]

    def create(self, validated_data):
        user = UserProfile(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            alternate_mobile_number=validated_data['alternate_mobile_number'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print(1000000,username)
        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

            else:
                msg = {'detail': 'username is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id","country", "state", "city", "pincode", "street_number", "permanent_address",
                  "type_of_address", "user"]
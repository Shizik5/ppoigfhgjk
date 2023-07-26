from django.contrib.auth import get_user_model
from rest_framework import serializers

from registration.models import *
from registration.send_sms import send_activation_sms

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=8, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, max_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email','password','password_confirmation', 'first_name','last_name','username')

    def validate(self,attrs):
        password = attrs['password']
        password_confirmation = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError(
                'пароли не совпадают'
            )

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'пароль должен содержать цифры и буквы'
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        self.code = attrs['code']
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()
        except:
            self.fail('неверный код')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)


class RegisterPhoneSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True, allow_null=True)
    password_confirmation = serializers.CharField(min_length=6, max_length=20, required=True,
                                                  write_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation',
                  'first_name', 'last_name', 'username', 'phone_number')

    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError(
                'пароли не совпадают'
            )

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'пароль должен содержать цифры и буквы'
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_sms(user.phone_number, user.activation_code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser, UserManager
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
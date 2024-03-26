# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PhoneNumber


    

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']

class UserSerializer(serializers.ModelSerializer):
    ph = PhoneNumberSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'ph', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        phone_number_data = validated_data.pop('ph', None)
        user = User.objects.create_user(**validated_data)
        if phone_number_data:
            PhoneNumber.objects.create(user=user, **phone_number_data)
        return user






from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise AuthenticationFailed(msg)
                return attrs
            else:
                msg = 'Unable to log in with provided credentials.'
                raise AuthenticationFailed(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise AuthenticationFailed(msg)









# from django.core.mail import send_mail
# from django.conf import settings

# class UserSerializer(serializers.ModelSerializer):
#     ph = PhoneNumberSerializer(required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'ph', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def create(self, validated_data):
#         phone_number_data = validated_data.pop('ph', None)
#         user = User.objects.create_user(**validated_data)
#         if phone_number_data:
#             PhoneNumber.objects.create(user=user, **phone_number_data)
        
#         # Sending welcome email
#         subject = 'Welcome to Our Website'
#         message = 'Thank you for registering with us!'
#         from_email = settings.EMAIL_HOST_USER
#         to_email = validated_data['email']
#         send_mail(subject, message, from_email, [to_email])

#         return user



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    ph = PhoneNumberSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'ph', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        phone_number_data = validated_data.pop('ph', None)
        user = User.objects.create_user(**validated_data)
        if phone_number_data:
            PhoneNumber.objects.create(user=user, **phone_number_data)
        
        # Sending welcome email
        subject = 'Welcome to Our Website'
        html_message = render_to_string('index.html', {'user': user})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = validated_data['email']
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return user







        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        










    
        
        
        
        
        


        
     


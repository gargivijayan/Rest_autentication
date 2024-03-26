from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import PhoneNumber
from .serializers import UserSerializer
from .models import User

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny  
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

class PhoneNumberListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    



 
@api_view(['POST'])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()
    if not user or not user.check_password(password):
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
    except TokenError:
        return Response({'error': 'Failed to generate tokens'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'access_token': str(access_token),
        'refresh_token': str(refresh_token),
    }, status=status.HTTP_200_OK)
    
       
    
class CustomAuthToken(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'refresh': str(refresh)
,
            'access': str(access_token),
            'user_id': user.pk,
            'username': user.username,
        }, status=status.HTTP_200_OK)
    
    


# views.py


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user_instance = self.get_object()
        serializer = self.get_serializer(user_instance)
        data = serializer.data
        return Response(data)






from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'access_token': access_token}, status=status.HTTP_200_OK)












from django.core.mail import send_mail
from django.conf import settings





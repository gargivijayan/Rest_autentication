from django.urls import path
from .views import PhoneNumberListView
from .views import custom_login
from .views import UserDetailView


from .views import RefreshTokenView


urlpatterns = [
    path('signup/',  PhoneNumberListView.as_view()), 
    path('api/login/', custom_login, name='custom_login'),
    path('api/user-detail/', UserDetailView.as_view(), name='user_detail'),
    
    
    path('api/token/refresh/', RefreshTokenView.as_view(), name='refresh_token'),

]







 





  
    


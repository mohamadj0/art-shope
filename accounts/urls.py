from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LoginOutUserView.as_view(), name='logout'),
]
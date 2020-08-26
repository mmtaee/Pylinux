from django.urls import path, include

from .views import *

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recover_activation/', ForgotActivationView.as_view(), name='forgot_activation'),
    path('activate/<str:uidb64>/<str:token>/',Activation.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    # handler test
    path('test/<int:status_code>/', HandlerTest.as_view()),
]
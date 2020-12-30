from django.urls import path
from . import views
from .views import ActivateAccount, SignUpView, AfterSignUpView


urlpatterns = [
    path('login/', views.signin, name='login'),
    path('logout/', views.LogoutViewMy.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeMy.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneMy.as_view(), name='password_change_done'),
    path("signup/", SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('signup/confirmation_email/', AfterSignUpView.as_view(), name='confirmation_email')
]

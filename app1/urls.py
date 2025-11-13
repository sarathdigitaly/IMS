from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, SignInView, UserProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
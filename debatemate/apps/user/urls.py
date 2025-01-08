from django.urls import path

from .views import (
    UserView,
    UserSearchView,
    UserSigninView,
    UserSignupView,
    UserSignupOTPView,
)

urlpatterns = [

    # アカウント検索
    path(
        route='',
        view=UserSearchView.as_view(),
        name='user',
    ),

    # サインイン
    path(
        route='signin/',
        view=UserSigninView.as_view(),
        name='user.signin',
    ),

    # サインアップ
    path(
        route='signup/',
        view=UserSignupView.as_view(),
        name='user.signup',
    ),

    # サインアップ後のOTPによるアクティブ化
    path(
        route='signup/otp/',
        view=UserSignupOTPView.as_view(),
        name='user.signup.otp',
    ),

    # アカウント詳細
    path(
        route='<uuid:user_id>/',
        view=UserView.as_view(),
        name='user.(id)',
    ),

]

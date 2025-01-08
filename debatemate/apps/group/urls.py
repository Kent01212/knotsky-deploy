from django.urls import path

from .views import (
    GroupView,
    GroupSearchView,
    GroupCreateView,
    GroupUserView,
    GroupUserSearchView,
    GroupUserInviteView,
    GroupUserInviteSearchView,
    GroupBotView,
    GroupBotSearchView,
    GroupBotInviteView,
    GroupBotInviteSearchView,
)


urlpatterns = [

    # グループ検索
    path(
        route='',
        view=GroupSearchView.as_view(),
        name='group',
    ),

    # グループ作成
    path(
        route='create/',
        view=GroupCreateView.as_view(),
        name='group.create',
    ),

    # グループ詳細
    path(
        route='<uuid:group_id>/',
        view=GroupView.as_view(),
        name='group.(id)',
    ),


    # グループユーザー検索
    path(
        route='<uuid:group_id>/user/',
        view=GroupUserSearchView.as_view(),
        name='group.(id).user',
    ),

    # グループユーザー詳細
    path(
        route='<uuid:group_id>/user/<uuid:user_id>/',
        view=GroupUserView.as_view(),
        name='group.(id).user.(id)',
    ),

    # グループユーザー招待
    path(
        route='<uuid:group_id>/user/invite/',
        view=GroupUserInviteSearchView.as_view(),
        name='group.(id).user.invite',
    ),

    # グループユーザー招待
    path(
        route='<uuid:group_id>/user/invite/<uuid:user_id>/',
        view=GroupUserInviteView.as_view(),
        name='group.(id).user.invite.(id)',
    ),


    # グループボット検索
    path(
        route='<uuid:group_id>/bot/',
        view=GroupBotSearchView.as_view(),
        name='group.(id).bot',
    ),

    # グループボット詳細
    path(
        route='<uuid:group_id>/bot/<uuid:bot_id>/',
        view=GroupBotView.as_view(),
        name='group.(id).bot.(id)',
    ),

    # グループボット招待
    path(
        route='<uuid:group_id>/bot/invite/',
        view=GroupBotInviteSearchView.as_view(),
        name='group.(id).bot.invite',
    ),

    # グループボット招待
    path(
        route='<uuid:group_id>/bot/invite/<uuid:bot_id>/',
        view=GroupBotInviteView.as_view(),
        name='group.(id).bot.invite.(id)',
    ),
]

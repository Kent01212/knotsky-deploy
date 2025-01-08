from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # ディベート
    path(
        route='debate/',
        view=include('debatemate.apps.debate.urls'),
    ),

    # ボット
    path(
        route='bot/',
        view=include('debatemate.apps.bot.urls'),
    ),

    # アカウント
    path(
        route='user/',
        view=include('debatemate.apps.user.urls'),
    ),

    # チャット
    path(
        route='chat/',
        view=include('debatemate.apps.chat.urls'),
    ),

    # グループ
    path(
        route='group/',
        view=include('debatemate.apps.group.urls'),
    ),
]

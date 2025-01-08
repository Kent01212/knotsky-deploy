from django.urls import path
from .views import BotDeleteView

from .views import (
    BotView,
    BotSearchView,
    BotCreateView,
)

urlpatterns = [

    # ボット検索
    path(
        route='',
        view=BotSearchView.as_view(),
        name='bot_search',
    ),

    # ボット詳細
    path(
        route='<int:id>/',
        view=BotView.as_view(),
        name='bot.(id)',
    ),

    # ボット作成
    path(
        route='create/',
        view=BotCreateView.as_view(),
        name='bot.create',
    ),

    
    path(
        route='bot/<int:id>/delete/', 
        view=BotDeleteView.as_view(), 
        name='bot_delete'
        ), 
]

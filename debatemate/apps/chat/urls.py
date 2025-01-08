from django.urls import path

from .views import (
    ChatView,
    ChatCreateView,
    ChatSearchView,
    ChatDeleteView,
)

urlpatterns = [

    # チャット検索
    path(
        route='',
        view=ChatSearchView.as_view(),
        name='chat',
    ),

    # チャット作成
    path(
        route='create/',
        view=ChatCreateView.as_view(),
        name='chat.create',
    ),

    # チャット詳細
    path(
        route='<str:chat_id>/',
        view=ChatView.as_view(),
        name='chat.(id)',
    ),

    # チャット削除 仮設置
    path(
        route='chat/<int:id>/delete/', 
        view=ChatDeleteView.as_view(), 
        name='chat_delete'
    ), 

]

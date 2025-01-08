# debatemate/apps/debate/urls.py
from django.urls import path

from .views import (
    DebateView,
    DebateSearchView,
    DebateCreateView,
)

urlpatterns = [

    # 議論検索
    path(
        route='',
        view=DebateSearchView.as_view(),
        name='debate',
    ),

    # 議論作成
    path(
        route='create/',
        view=DebateCreateView.as_view(),
        name='debate.create',
    ),

    # 議論詳細
    path(
        route='<uuid:debate_id>/',
        view=DebateView.as_view(),
        name='debate.(id)',
    ),
]

# debatemate/apps/debate/views.py
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Debate, DebateUser, DebateMessage
from django.db.models import Prefetch
from .forms import DebateSearchForm, DebateCreateForm
from .models import Debate, DebateUser, DebateMessage
from django.contrib.auth import get_user_model
import json
from typing import Union

User = get_user_model()

class DebateView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, debate_id: str) -> HttpResponse:
        debate = get_object_or_404(Debate, id=debate_id)

        # デベート参加者の取得
        debate_users = DebateUser.objects.filter(debate=debate).select_related('user')
        users = [
            {
                'id': du.user.id,
                'name': du.user.name,
                'icon': du.user.icon.url if du.user.icon else None,
                'about': du.user.about
            } for du in debate_users
        ]

        # メッセージの取得と整形
        messages = DebateMessage.objects.filter(
            author__debate=debate
        ).select_related(
            'author__user'
        ).order_by('created_at')

        formatted_messages = [
            {
                'id': msg.id,
                'content': msg.content,
                'author': msg.author.user.name,
                'author_icon': msg.author.user.icon.url if msg.author.user.icon else None,
                'timestamp': msg.created_at.strftime("%Y-%m-%d %H:%M"),
                'is_own': msg.author.user == request.user
            } for msg in messages
        ]

        # API リクエストの場合
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'messages': formatted_messages,
                'users': users
            })

        context = {
            'debate': debate,
            'users': users,
            'messages': formatted_messages,
            'user': request.user,
        }

        return render(request, 'debate.html', context)

    def post(self, request: HttpRequest, debate_id: str) -> Union[HttpResponse, JsonResponse]:
        debate = get_object_or_404(Debate, id=debate_id)

        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                message_content = data.get('message')
            else:
                message_content = request.POST.get('message')

            if not message_content:
                return JsonResponse({'error': 'Message content is required'}, status=400)

            # ユーザーの取得または作成
            debate_user, created = DebateUser.objects.get_or_create(
                debate=debate,
                user=request.user
            )

            # メッセージの作成
            message = DebateMessage.objects.create(
                content=message_content,
                author=debate_user
            )

            # WebSocketを通じて送信するためのレスポンスデータ
            response_data = {
                'id': message.id,
                'content': message.content,
                'author': message.author.user.name,
                'author_icon': message.author.user.icon.url if message.author.user.icon else None,
                'timestamp': message.created_at.strftime("%Y-%m-%d %H:%M"),
                'is_own': True
            }

            if request.content_type == 'application/json':
                return JsonResponse(response_data)

            return self.get(request, debate_id)

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)




class DebateCreateView(View):

    def get(self, request: HttpRequest):
        form = DebateCreateForm()
        return render(request, 'debate_create.html', {
            'form': form,

        })

    def post(self, request: HttpRequest):
        return render(request, 'debate_create.html')


class DebateSearchView(View):

    def get(self, request: HttpRequest):

        # フォームを初期化
        # →最初なので空
        form = DebateSearchForm()

        # デベートを全件取得
        debates = Debate.objects.all()

        # テンプレートに渡す
        return render(request, 'debate_search.html', {
            'form': form,
            'debates': debates
        })

    def post(self, request: HttpRequest):

        # フォームを取得
        # →最初なので空
        form = DebateSearchForm(request.POST)

        # 検索フォームの検証
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリ
        query = form.cleaned_data['query']

        # クエリが空文字列なら204を返す
        if not query:
            return HttpResponse(status=204)

        # デベートを全件取得
        debates = Debate.objects.filter(title__icontains=query)

        # テンプレートに渡す
        return render(request, 'debate_search.html', {
            'form': form,
            'debates': debates
        })

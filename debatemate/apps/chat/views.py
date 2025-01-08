from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from debatemate.apps.group.models import Group

from .forms import (
    ChatSearchForm,
    ChatMessageForm,
    ChatCreateForm,
)

from .models import (
    Chat,
    ChatMessage,
)


# Create your views here.
class ChatView(View):

    template_name = 'chat.html'

    def get(self, request: HttpRequest, chat_id: str):

        # チャットを取得
        chat = get_object_or_404(Chat, id=chat_id)

        # チャットリストを取得
        chats = Chat.objects.filter(group=chat.group)

        # メッセージを取得
        messages = ChatMessage.objects.filter(chat=chat).order_by('created_at')

        # フォームの初期化
        form = ChatMessageForm()

        # 画面表示
        return render(request, self.template_name, {
            'group': chat.group,
            'chat': chat,
            'chats': chats,
            'form': form,
            'messages': messages
        })

    def post(self, request: HttpRequest, chat_id: str):

        # チャットを取得
        chat = get_object_or_404(Chat, id=chat_id)

        # グループを取得
        chats = Chat.objects.filter(group=chat.group)

        # フォームを取得
        form = ChatMessageForm(request.POST)

        # フォームの検証
        if not form.is_valid():
            return HttpResponse(status=200)

        # メッセージを作成
        ChatMessage.objects.create(
            chat=chat,
            user=request.user,
            message=form.cleaned_data['message'],
        )

        # メッセージを取得
        messages = ChatMessage.objects.filter(chat=chat).order_by('created_at')

        # 画面表示
        return render(request, self.template_name, {
            'chat': chat,
            'chats': chats,
            'form': form,
            'messages': messages
        })


class ChatCreateView(View):
    template_name = 'chat_create.html'

    def get(self, request: HttpRequest):
        # 空のフォームを生成してレンダリング
        form = ChatCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        # リクエストデータを用いてフォームを生成
        form = ChatCreateForm(request.POST)
        if form.is_valid():
            # フォームのデータを使ってチャットを作成
            Chat.objects.create(name=form.cleaned_data['name'])
        # フォームが無効の場合は再レンダリング
        return render(request, self.template_name, {'form': form})


class ChatSearchView(View):

    template_name = 'chat_search.html'

    def get(self, request: HttpRequest):

        # フォームの初期化
        # →最初なので空
        form = ChatSearchForm()

        # グループ内のチャットを取得
        # →取得したクエリを利用して検索
        chats = Chat.objects.all()

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'chats': chats
        })

    def post(self, request: HttpRequest):

        # フォームを取得
        form = ChatSearchForm(request.POST)

        # 検索フォームが正しい形式ではない場合
        # →204を返す
        if not form.is_valid():
            return HttpResponse(status=200)

        # 検索クエリ
        query = form.cleaned_data['query']

        # クエリが空文字列なら204を返す
        if not query:
            return HttpResponse(status=204)

        # デベートを全件取得
        chats = Chat.objects.filter(name__icontains=query)

        # テンプレートに渡す
        return render(request, 'chat_search.html', {
            'form': form,
            'chats': chats
        })

# 仮設置
class ChatDeleteView(View):
    def post(self, request: HttpRequest, id: int):
        chat = get_object_or_404(chat, id=id)
        
        # # 削除権限を確認（オプション）
        # if chat.owner != request.user:
        #     return HttpResponse(status=403)  # 権限がない場合

        chat.delete()
        return HttpResponseRedirect(reverse('chat_search'))  # ボット一覧ページにリダイレクト
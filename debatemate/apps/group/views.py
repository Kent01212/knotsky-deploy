import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from debatemate.apps.user.models import User
from debatemate.apps.bot.models import Bot

from .forms import (
    GroupForm,
    GroupSearchForm,
    GroupCreateForm,
    GroupBotSearchForm,
    GroupBotInviteSearchForm,
    GroupUserSearchForm,
    GroupUserInviteSearchForm
)

from .models import (
    Group,
    GroupBot,
    GroupUser,
)


class GroupView(LoginRequiredMixin, View):

    """
    グループ詳細画面
    """

    template_name = 'group.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID):

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループ編集フォーム
        # →最初なので空
        form = GroupForm()
        form.name = group.name
        form.icon = group.icon
        form.description = group.description

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group': group
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID):

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループ編集フォーム
        # →リクエストで編集フォームを取得
        form = GroupForm(request.POST)

        # 検索フォームの検証
        # →検索フォームに値がない場合には204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # グループ編集
        group = Group(**form.cleaned_data)
        group.save()

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group': group
        })


class GroupCreateView(LoginRequiredMixin, View):

    """
    グループ作成画面
    """

    template_name = 'group_create.html'

    def get(self, request: HttpRequest):

        # グループ作成フォーム
        # →最初なので空
        form = GroupCreateForm()

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request: HttpRequest):

        # グループ作成フォーム
        # →リクエストで作成フォームを取得
        form = GroupCreateForm(request.POST)

        # 検索フォームの検証
        # →検索フォームに値がない場合には204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリが空文字列の場合
        # →204を返す
        group, created =\
            Group.objects.get_or_create(name=form.cleaned_data['name'])

        # グループ名重複チェック
        if not created:
            return HttpResponse(status=204)

        # 画面表示
        return redirect('group', group_id=group.id)


class GroupSearchView(LoginRequiredMixin, View):

    """
    グループ検索画面
    """

    template_name = 'group_search.html'

    def get(self, request: HttpRequest):

        # グループ検索フォーム
        form = GroupSearchForm()

        # グループ一覧
        groups = Group.objects.all()

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'groups': groups
        })

    def post(self, request: HttpRequest):

        # グループ検索フォーム
        # →リクエストで検索フォームを取得
        form = GroupSearchForm(request.POST)

        # 検索フォームの検証
        # →検索フォームに値がない場合には204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリ
        # →検索フォームから取得
        query = form.cleaned_data['query']

        # グループを全件取得
        # →取得したクエリを利用して検索
        if not query:
            return HttpResponse(status=204)

        # グループを全件取得
        group_users =\
            GroupUser.objects.filter(user=request.user)

        # 検索フォームの検証
        groups = group_users\
            .filter(group__title__icontains=query)\
            .values_list('group', flat=True)

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'groups': groups
        })


class GroupUserView(LoginRequiredMixin, View):

    """
    グループユーザー画面
    """

    template_name = 'group_user.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name, {})

    def post(self, request: HttpRequest):
        return render(request, self.template_name, {})


class GroupUserSearchView(LoginRequiredMixin, View):

    """
    グループユーザー検索画面
    """

    template_name = 'group_user_search.html'

    def get(self, request: HttpRequest, group_id: int):

        # グループ検索フォーム
        # →グループ検索フォームを初期化
        form = GroupUserSearchForm()

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループアカウントのコレクション
        # →取得したクエリを利用して検索
        group_users = GroupUser.objects.filter(group=group)

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group_users': group_users,
            'group': group
        })

    def post(self, request: HttpRequest, group_id: int):

        # グループ検索フォーム
        # →リクエストで検索フォームを取得
        form = GroupUserSearchForm(request.POST)

        # 検索フォームが正しい形式ではない場合
        # →204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリを取得
        query = form.cleaned_data['query']

        # 検索クエリが空文字列の場合
        # →204を返す
        if not query:
            return HttpResponse(status=204)

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループアカウントのコレクション
        # →取得したクエリを利用して検索
        group_users =\
            GroupUser.objects.filter(group=group, nickname__icontains=query)

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group_users': group_users,
            'group': group
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID, user_id: uuid.UUID):

        # グループ検索フォーム
        # →リクエストで検索フォームを取得
        user = get_object_or_404(User, id=user_id)

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # 権限チェック
        if True:
            GroupUser.objects.get_or_create(group=group, user=user)

        # グループを取得
        return render(request, self.template_name, {
            'user': user,
            'group': group,
            'is_invited': True
        })


class GroupUserInviteSearchView(LoginRequiredMixin, View):

    """
    グループユーザー招待検索画面
    """

    template_name = 'group_user_invite_search.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID):

        # グループ検索フォーム
        # →グループ検索フォームを初期化
        form = GroupUserInviteSearchForm()

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # ユーザーを取得
        # →存在しないユーザーIDの場合には404を返す
        users = User.objects.all()

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group': group,
            'users': users
        })


class GroupUserInviteView(LoginRequiredMixin, View):

    """
    グループユーザー招待画面
    """

    template_name = 'group_user_invite.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID, user_id: uuid.UUID):

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループ検索フォーム
        # →グループ検索フォームを初期化
        user = get_object_or_404(User, id=user_id)

        # 権限チェック
        if True:
            GroupUser.objects.get_or_create(group=group, user=user)

        # 招待済みフラグ
        is_invited =\
            GroupUser.objects.filter(group=group, user=user).exists()

        # 画面表示
        return render(request, self.template_name, {
            'group': group,
            'user': user,
            'is_invited': is_invited,
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID, user_id: uuid.UUID):

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループ検索フォーム
        # →グループ検索フォームを初期化
        user = get_object_or_404(User, id=user_id)

        # 権限チェック
        if True:
            GroupUser.objects.get_or_create(group=group, user=user)

        # 招待済みフラグ
        is_invited = GroupUser.objects.exists(group=group, user=user)

        # 画面表示
        return render(request, self.template_name, {
            'group': group,
            'user': user,
            'is_invited': is_invited,
        })


class GroupBotView(LoginRequiredMixin, View):

    """
    グループBot画面
    """

    template_name = 'group_bot.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID, bot_id: uuid.UUID):
        return render(request, self.template_name, {})

    def post(self, request: HttpRequest, group_id: uuid.UUID, bot_id: uuid.UUID):
        return render(request, self.template_name, {})


class GroupBotSearchView(LoginRequiredMixin, View):

    """
    グループBot検索画面
    """

    template_name = 'group_bot_search.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID):

        # グループBot検索フォーム
        # →グループBot検索フォームを初期化
        form = GroupBotInviteSearchForm()

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループBotのコレクション
        # →取得したクエリを利用して検索
        group_bots = GroupBot.objects.filter(group=group)

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group_bots': group_bots,
            'group': group
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID):

        # グループBot検索フォーム
        # →リクエストで検索フォームを取得
        form = GroupBotInviteSearchForm(request.POST)

        # 検索フォームの検証
        # →検索フォームに値がない場合には204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリを取得
        # →存在しないGroupIDの場合には404を返す
        query = form.cleaned_data['query']

        # 検索クエリが空文字列の場合
        # →204を返す
        if not query:
            return HttpResponse(status=204)

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループBotのコレクション
        # →取得したクエリを利用して検索
        group_bots =\
            GroupBot.objects.filter(group=group, nickname__icontains=query)

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group_bots': group_bots,
            'group': group
        })


class GroupBotInviteSearchView(LoginRequiredMixin, View):

    """
    グループBot招待検索画面
    """

    template_name = 'group_bot_invite_search.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID):

        # グループBot検索フォーム
        # →グループBot検索フォームを初期化
        form = GroupBotSearchForm()

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # グループBotのコレクション
        # →取得したクエリを利用して検索
        group_bots = GroupBot.objects.all()

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'group_bots': group_bots,
            'group': group,
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID):

        # グループBot検索フォーム
        # →リクエストで検索フォームを取得
        form = GroupBotSearchForm(request.POST)

        # 検索フォームの検証
        # →検索フォームに値がない場合には204を返す
        if not form.is_valid():
            return HttpResponse(status=204)

        # 検索クエリが空文字列の場合
        # →204を返す
        query = form.cleaned_data['query']

        # 検索クエリが空文字列の場合
        # →204を返す
        if not query:
            return HttpResponse(status=204)

        # グループBotのコレクション
        # →取得したクエリを利用して検索
        bots = Bot.objects.filter(name__icontains=query)

        # グループを取得
        # →存在しないGroupIDの場合には404を返す
        group = get_object_or_404(Group, id=group_id)

        # 画面表示
        return render(request, self.template_name, {
            'form': form,
            'bots': bots,
            'group': group,
        })


class GroupBotInviteView(LoginRequiredMixin, View):

    template_name = 'group_bot_invite.html'

    def get(self, request: HttpRequest, group_id: uuid.UUID, bot_id: uuid.UUID):

        # グループBot招待フォーム
        # →グループBot招待フォームを初期化
        group = get_object_or_404(Group, id=group_id)

        # グループBot検索フォーム
        # →グループBot検索フォームを初期化
        bot = get_object_or_404(Bot, id=bot_id)

        # 招待済みフラグ
        is_invited = GroupBot.objects.exists(group=group, bot=bot)

        # 画面表示
        return render(request, self.template_name, {
            'group': group,
            'bot': bot,
            'is_invited': is_invited
        })

    def post(self, request: HttpRequest, group_id: uuid.UUID, bot_id: uuid.UUID):

        # グループBot招待フォーム
        # →リクエストでグループBot招待フォームを取得
        group = get_object_or_404(Group, id=group_id)

        # グループBot招待
        # →グループBot招待を行う
        bot = get_object_or_404(Bot, id=bot_id)

        # グループBot招待
        if True:
            GroupBot.objects.get_or_create(group=group, bot=bot)

        # 招待済みフラグ
        is_invited = GroupBot.objects.exists(group=group, bot=bot)

        # グループBot招待フォーム
        # →リクエストでグループBot招待フォームを取得
        return render(request, self.template_name, {
            'group': group,
            'bot': bot,
            'is_invited': is_invited
        })

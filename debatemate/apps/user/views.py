import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    UserSearchForm,
    UserSigninForm,
    UserSignupForm,
    UserSignupOTPForm,
)

from .models import (
    User,
    UserOTP,
)

from .settings import (
    SIGNUP_OTP_URL,
    SIGNUP_OTP_REDIRECT_URL,
)


class UserSearchView(LoginRequiredMixin, View):

    template_name = 'user_search.html'

    def get(self, request: HttpRequest):

        # グループ検索フォーム
        # →最初なので空
        form = UserSearchForm()

        # グループを全件取得
        # →取得したクエリを利用して検索
        users = User.objects.all()

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'users': users
        })

    def post(self, request: HttpRequest):

        # グループ検索フォーム
        # →リクエストで検索フォームを取得
        form = UserSearchForm(request.POST)

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

        # 検索フォームの検証
        users = User.objects.filter(name__icontains=query)

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'users': users
        })


class UserView(View):

    template_name = 'user.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name, {})

    def post(self, request: HttpRequest):
        return render(request, self.template_name, {})


class UserSigninView(View):

    template_name = 'user_signin.html'

    def get(self, request: HttpRequest):

        # フォームの初期化
        form = UserSigninForm()

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request: HttpRequest):

        # サインインフォームを生成
        # →最初なので空
        form = UserSigninForm(request.POST)

        # フォームの検証に失敗した場合
        # →200を返す
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form
            })

        # アカウントの資格情報を検証
        # →存在しない場合には404を返す
        user: User = authenticate(
            request=request,
            name=form.cleaned_data['name'],
            password=form.cleaned_data['password']
        )

        if not user:
            return HttpResponse(status=204)

        # 資格情報の検証に失敗した場合
        # →200を返す
        # if user is None or not user.is_active:
        # return HttpResponse(status=204)

        # 資格情報の検証に成功した場合
        # →ログインする
        login(request, user)

        # ベース画面または遷移画面へリダイレクト
        return redirect(request.GET.get('next', 'group'))


class UserSignupView(View):

    template_name = 'user_signup.html'

    def get(self, request: HttpRequest):

        # フォームの初期化
        # →最初なので空
        form = UserSignupForm()

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request: HttpRequest):

        # サインアップフォームを生成
        form = UserSignupForm(request.POST)

        # フォームの検証に失敗した場合
        # →ステップを維持し、再入力を求める
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
            })

        # パスワードと確認用パスワードを取得
        password =\
            form.cleaned_data['password']

        passowrd_confirmation =\
            form.cleaned_data['password_confirmation']

        # パスワードと確認用パスワードが一致しない場合
        if password != passowrd_confirmation:
            return render(request, self.template_name, {
                'form': form,
            })
        else:
            del form.cleaned_data['password_confirmation']

        # アカウントを作成
        user: User = User.objects.create_user(**form.cleaned_data)

        # アカウントをセッションに保存
        request.session['user_id'] = str(user.id)

        # リダイレクト
        return redirect('/user/signup/otp/')


class UserSignupOTPView(View):

    """
    OTP を送信する
    """

    template_name = 'user_signup_otp.html'

    def get(self, request: HttpRequest):

        # ユーザーIDを取得
        user_id = request.session.get('user_id')

        # ユーザーIDを持たない場合
        if user_id is None:
            return redirect('/user/signin/', next='/user/signup/otp/')

        # ユーザーIDをUUIDに変換
        user_id = uuid.UUID(user_id)

        # ユーザーを取得
        user = get_object_or_404(User, id=user_id)

        # OTP用のフォームを取得
        # →最初なので空
        form = UserSignupOTPForm()

        # アカウントのOTPを作成
        user_otp = UserOTP.objects.create(user=user)

        # アカウントのOTPを送信
        user_otp.issue_token_and_send(user.email)

        # テンプレートに渡す
        return render(request, self.template_name, {
            'form': form,
            'user': user
        })

    def post(self, request: HttpRequest):

        # OTP用のフォームを取得
        form = UserSignupOTPForm(request.POST)

        # フォームの検証に失敗した場合
        # →ステップを維持し、再入力を求める
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form
            })

        # ユーザーIDを取得
        user_id = request.session.get('user_id')

        # ユーザーIDを持たない場合
        if user_id is None:
            return HttpResponse(status=204)

        # アカウントを取得
        user = get_object_or_404(User, id=user_id)

        # アカウントOTPを取得
        user_otp = get_object_or_404(UserOTP, user=user)

        # user OTP の検証に失敗した場合
        # →ステップを維持し、再入力を求める
        if not user_otp.check_token(**form.cleaned_data):
            return render(request, self.template_name, {
                'form': form
            })

        # アカウントを有効化
        user.is_active = True
        user.save()

        # ユーザーのOTPを削除
        del request.session['user_id']

        # ログイン
        login(request, user)

        # ベース画面または遷移画面へリダイレクト
        return redirect(request.GET.get('next', '/group/'))


class UserRecoverView(View):

    template_1_name = 'user_recover_1.html'
    template_2_name = 'user_recover_2.html'
    template_3_name = 'user_recover_3.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name, {})

    def post(self, request: HttpRequest):
        return render(request, self.template_name, {})

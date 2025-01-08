from django import forms
from django.core.validators import RegexValidator


class UserSigninForm(forms.Form):

    name_attrs = {
        'type': 'text',
        'placeholder': 'ユーザー名'
    }

    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs),
    )

    password_attrs = {
        'type': 'password',
        'placeholder': 'パスワード'
    }

    password = forms.CharField(
        required=True,
        max_length=255,
        min_length=8,
        widget=forms.PasswordInput(attrs=password_attrs),
        validators=[RegexValidator(regex=r'[A-Za-z0-9]+')]
    )


class UserSignupForm(forms.Form):

    name_attrs = {
        'type': 'text',
        'placeholder': 'ユーザー名'
    }

    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs),
    )

    email_attrs = {
        'type': 'email',
        'placeholder': 'メールアドレス'
    }

    email = forms.EmailField(
        required=True,
        max_length=255,
        widget=forms.EmailInput(attrs=email_attrs),
    )

    password_attrs = {
        'type': 'password',
        'placeholder': 'パスワード'
    }

    password = forms.CharField(
        required=True,
        max_length=255,
        min_length=8,
        widget=forms.PasswordInput(attrs=password_attrs),
        validators=[RegexValidator(regex=r'[A-Za-z0-9]+')]
    )

    password_confirmation_attrs = {
        'type': 'password',
        'placeholder': 'パスワード（確認）'
    }

    password_confirmation = forms.CharField(
        required=True,
        max_length=255,
        min_length=8,
        widget=forms.PasswordInput(attrs=password_confirmation_attrs),
        validators=[RegexValidator(regex=r'[A-Za-z0-9]+')]
    )


class UserSignupOTPForm(forms.Form):

    token_attrs = {
        'type': 'text',
        'placeholder': 'XXXXXXXX'
    }

    token = forms.CharField(
        required=True,
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs=token_attrs),
        validators=[RegexValidator(regex=r'[0-9A-Z]{8}')]
    )


class UserSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.TextInput(attrs=query_attrs)
    )

from django import forms


class GroupForm(forms.Form):

    name_attrs = {
        'type': 'text',
        'placeholder': 'グループ名を入力'
    }

    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs)
    )

    icon_attrs = {
        'type': 'file',
        'placeholder': 'アイコンを選択'
    }

    icon = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs=icon_attrs)
    )

    description_attrs = {
        'type': 'text',
        'placeholder': '説明を入力'
    }

    description = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.Textarea(attrs=description_attrs)
    )


class GroupSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.TextInput(attrs=query_attrs)
    )


class GroupCreateForm(forms.Form):

    name_attrs = {
        'type': 'text',
        'placeholder': '作成するグループ名を入力'
    }

    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs)
    )


class GroupUserSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.TextInput(attrs=query_attrs)
    )


class GroupUserInviteSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
    )


class GroupBotSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.TextInput(attrs=query_attrs)
    )


class GroupBotInviteSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        required=True,
        max_length=1024,
    )

from django import forms


class ChatSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=True,
        label='検索ワード',
        widget=forms.TextInput(attrs={'placeholder': 'チャット名を入力してください'})
    )


class ChatMessageForm(forms.Form):

    message_attrs = {
        'type': 'text',
        'placeholder': 'メッセージを入力してください'
    }

    message = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.TextInput(attrs=message_attrs)
    )

class ChatCreateForm(forms.Form):
    name_attrs = {
        'type': 'text',
        'placeholder': 'チャット名を入力してください'
    }

    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs)
    )

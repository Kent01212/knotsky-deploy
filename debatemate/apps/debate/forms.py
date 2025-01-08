from django import forms


class DebateSearchForm(forms.Form):

    query = forms.CharField(
        max_length=255,
        required=True,
        label='検索ワード',
        widget=forms.TextInput(attrs={'placeholder': '検索ワードを入力してください'})
    )


class DebateCreateForm(forms.Form):

    name_attrs = {
        'type': 'text',
    }

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs=name_attrs),
    )

    bot_name_attrs = {
        'type': 'text',
    }

    bot_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs=bot_name_attrs),
    )

    description_attrs = {
        'type': 'text',
    }

    description = forms.CharField(
        max_length=4096,
        widget=forms.Textarea(attrs=description_attrs),
    )

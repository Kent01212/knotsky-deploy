from django import forms
from .models import Bot


class BotSearchForm(forms.Form):

    query_attrs = {
        'type': 'text',
        'placeholder': '検索ワードを入力してください'
    }

    query = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(attrs=query_attrs)
    )

class BotConfigForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name', 'icon', 'description']
        labels = {
            'name': 'ボット名',
            'icon': 'アイコン',
            'discription': '説明',
        }
        widgets = {
            'discription': forms.Textarea(attrs={'rows': 6}),
            'icon': forms.FileInput(),

            }

class BotCreateForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name', 'icon', 'description']
        labels = {
            'name': 'ボット名',
            'icon': 'アイコン',
            'description': '説明',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ボット名を入力してください'}),
            'icon': forms.FileInput(),
            'description': forms.Textarea(attrs={'placeholder': 'ボットの説明を入力してください'}),
        }
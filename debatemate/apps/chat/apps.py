from django.apps import AppConfig
from django import forms

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'debatemate.apps.chat'

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)  # ファイルのアップロードを許可
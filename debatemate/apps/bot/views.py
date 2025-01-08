from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from .models import Bot
from debatemate.apps.user.models import User
from .forms import BotSearchForm, BotConfigForm, BotCreateForm
# Create your views here.


class BotView(View):
    template_name = 'bot_config.html'

    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get('id')
        bot = get_object_or_404(Bot, id=bot_id)
        form = BotConfigForm(instance=bot)
        return render(request, self.template_name, {'form': form, 'bot': bot})

    def post(self, request, *args, **kwargs):
        bot_id = kwargs.get('id')
        bot = get_object_or_404(Bot, id=bot_id)
        form = BotConfigForm(request.POST, request.FILES, instance=bot)  # request.FILESを追加
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form, 'bot': bot})

class BotCreateView(View):
    template_name = 'bot_create.html'

    def get(self, request: HttpRequest):
        form = BotCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        form = BotCreateForm(request.POST, request.FILES)
        if form.is_valid():
            bot = form.save(commit=False)
            # bot.owner = request.user  # 現在ログイン中のユーザーを設定
            bot.owner = User.objects.first()
            bot.save()
            return redirect('bot_search')
        return render(request, self.template_name, {'form': form})


class BotSearchView(View):

    template_name = 'bot_search.html'

    def get(self, request: HttpRequest):
        form = BotSearchForm()

        bots = Bot.objects.all()

        return render(request, self.template_name, {
            'form': form,
            'bots': bots
        })

    def post(self, request: HttpRequest):
        form = BotSearchForm(request.POST)

        if not form.is_valid():
            return HttpResponse(status=204)

        if not form.cleaned_data['query']:
            return HttpResponse(status=204)

        bots = Bot.objects.filter(name__icontains=form.cleaned_data['query'])

        return render(request, self.template_name, {
            'form': form,
            'bots': bots
        })

class BotDeleteView(View):
    def post(self, request: HttpRequest, id: int):
        bot = get_object_or_404(Bot, id=id)
        
        # # 削除権限を確認（オプション）
        # if bot.owner != request.user:
        #     return HttpResponse(status=403)  # 権限がない場合

        bot.delete()
        return HttpResponseRedirect(reverse('bot_search'))  # ボット一覧ページにリダイレクト
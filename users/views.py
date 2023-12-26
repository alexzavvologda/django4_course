from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView

from news.utils import get_client_ip
from .forms import *
from .models import *

from django.contrib.auth.models import User, Group

from .utils import send_mail_to_admin


# Create your views here.


def index(request):
    return render(request,'news/profil.html')


# def register(request):
#     return render(request,'news/register.html')
#
# def register_2(request):
#     return render(request,'news/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Вы разлогинились')
    #return HttpResponseRedirect(reverse('news:news', args=['all', '0']))
    return HttpResponseRedirect(reverse('news:index'))
    #return render(request, '/' )


def login_user(request):
    # print('зашли в юсер вью')
# class login_user(View):
#     def post(self):
    #https://docs.djangoproject.com/en/4.2/topics/auth/default/
    if request.method == 'POST':
        # print('зашли ПОСТ')
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail_to_admin('Попытка авторизации', 'Попытка авторизации пользователь - ' + cd['login'] + '/ с адреса' + get_client_ip(request))
            #print(cd)
            #print('888888888888')
            #print(request.POST)
            user = authenticate(request, username=cd['login'], password=cd['password'])

            if user is not None:
            #if user and user.is_active:
                login(request, user)
                messages.success(request, 'Вы вошли')
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('users:profil'))
        else:
            # print('errrrrrrrrrrrrrrr')
            #return HttpResponseRedirect(reverse('users:profil'))
            messages.success(request, 'Ошибка')
            render(request, 'news/login.html', {'form_login': form})

            #     # Return an 'invalid login' error message.
            #return HttpResponseRedirect(reverse('/'))
            #return HttpResponseRedirect(reverse('/'))
            #return redirect('/')
    else:
        # print('зашли не ПОСТ')
        form = LoginForm()
        # print('222222222222222222222222222')
    # print('22555555555555555')
    return render(request,'news/login.html',{'form_login' : form })



# class CreateUserView(CreateView):
#     model = User
#     fields = ['username','password',  'first_name', 'last_name','email']
#     template_name = 'news/register.html'
#     #success_url = 'users:profil'
#     success_url = '/'

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    #model = User
    #fields = ['username','password',  'first_name', 'last_name','email']
    template_name = 'news/register.html'
    #success_url = 'users:profil'
    success_url = '/'
# передела через скрипт вверху через генерик
# чтобы потренироваться с добавлением групп
def RegisterUserScript(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save() # момент моздания пользователя
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Actions Required')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # надо создать аккаунт в связанной таблице, что бы было
            account = Account.objects.create(user=user,nickname=user.username)

            authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,f'{username} - зарегистрирован!')
            send_mail_to_admin('Создан пользователь',
                               'Создан пользователь - ' + username + '/ с адреса' + get_client_ip(
                                   request))
            return redirect('/')
    else:
        form = RegisterUserForm()
    context = {'form' : form}
    return render(request,'news/register.html',context)

# добавление удаление из избранного
from django.contrib.auth.decorators import login_required
from news.models import Article
@login_required(login_url = 'users:login')
def add_to_favorites(request,id):
    article = Article.objects.get(id=id)
    # проверим есть ли такая новость в избранном от этого пользователя
    bookmark = FavoriteArticle.objects.filter(user=request.user.id, article=article)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request,f'Новость  {article.title} удалена из закладок')
    else:
        bookmark = FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request, f'Новость  {article.title} добавлена в закладки')
    #return redirect('news:news')
    #отправить его назад откуда пришел
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


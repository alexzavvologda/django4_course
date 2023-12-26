from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.redirects.models import Redirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
import json
from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404, JsonResponse, \
    HttpResponseBadRequest
from django.views.generic import DetailView

from .models import Article, User, Tag, Categories, Image
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# https://docs.djangoproject.com/en/4.2/topics/auth/default/

from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Count

# decorator наш декоратор на проверку вхождения в группу
from users.utils import check_group, send_mail_to_admin

from django.contrib import messages

# что бы отправить на 404
# raise Http404

# # делим список list на наборы например по 3
# p = Paginator(list,3)
# # колличество сколько всего переадли в пагинатор
# p.count
# # кол-во страниц с блоками по 3 - сколько получилось - др словами на сколько страниц разбили наш словарь
# p.num_pages
# # итеротор с помощью его перебираем номера страниц
# p.page_range(1,5)
# # получить номер желаемой страницы-блок с кучкой статей разбитых по 3 вначале
# p1 = p.page(1)
# # получим список статей первлой страницы
# p1.object_list
# # признак существует ли следующая страница
# p1.has_next() False True
# # аналогично предыдущая страница
# p1.has_previous()
# # существует ли другие страницы
# p1.has_other_pages()
# # дайте номер следующей старницы
# p1.next_page_number()





# revers
#https://djangodoc.ru/3.1/ref/urlresolvers/#:~:text=%D0%AD%D1%82%D0%B0%20%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8F%20reverse()%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%D1%87%D0%B5%D1%80%D1%82%D0%BE%D0%B9%20(%20%22%7C%22%20).
# Create your views here.

# проверить разрешения
#@permission_required("polls.add_choice")

# user = request.user #the user
#      email = user.email #their email
#      username = user.username


def index(request):
    #raise Http404
    return render(request,'news/index.html')


'''
all_news = Article.objects.all().values('author','title')
    for a in all_news:
        print(a['author'], a['title'])
    all_news = Article.objects.all().values_list('author','title')
    for a in all_news:
        print(a)
        
        
article = Article.objects.get(id=1)
    print(article.author.username)
    
    
    
    # пример аннотирования и агрегации:
    max_article_count_user = User.objects.annotate(Count('article', distinct=True)).order_by('-article__count').first()
    print(max_article_count_user)
    max_article_count =  User.objects.annotate(Count('article', distinct=True)).aggregate(Max('article__count'))
    max_article_count_user2 = User.objects.annotate(Count('article', distinct=True)).filter(article__count__exact=max_article_count['article__count__max'])
    print(max_article_count_user2)



import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())
        
        
        class Meta:
        objects = models.Manager()
        published = PublishedToday()class Meta:
        objects = models.Manager()
        published = PublishedToday()
        
'''




@check_group('Authors')
def contacts(request):
    return render(request,'news/contacts.html')


#@login_required()
def news_all(request):

    #
    #Надо ко всем запросам поставить select_related
    #пример
    #ar = Article.objects.select_related('author'.get(pk=1))
    #для связи много ко многим нужно prefetch_related
    #  надо делать через prefetch_related
    #article_tags = Article.objects.prefetch_related('tags').get(id=1)
    context = {}
    context['categories'] = Categories.categoriesenable.all()
    context['news_spisok_rigth'] = Article.articleenable.select_related('category').prefetch_related('tags').all().order_by('-date')[:3]
    context['filtr_type'] = 'all'
    context['tags'] = Tag.objects.all()
    if request.method == 'POST':
        article_find_text = request.POST.get('article_find_text')
        article_find_by = request.POST.get('article_find_by')
        #print(article_find_text,'  строка поиска текста' )
        #print(article_find_by, '  какой выбор сделали')
        #print(request.POST)
        if article_find_by == 'by_text':
            news = Article.articleenable.select_related('category').prefetch_related('tags').filter(text__icontains=article_find_text)
        elif article_find_by == 'by_title':
            news = Article.articleenable.select_related('category').prefetch_related('tags').filter(title__icontains=article_find_text)
        context['news'] = news
    else:
        print('get')
        news = Article.articleenable.select_related('category').prefetch_related('tags').all()
        # пагинатор
        paginator = Paginator(news, 4)
        page_number = request.GET.get('page')
        print(page_number,'page_number')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['filtr_type'] = 'all'
        context['news'] = news

        return render(request, 'news/news_paginator.html', context)
    return render(request,'news/news.html', context)

def news_filtr(request, filtr_type, filtr_val):
#
#Надо ко всем запросам поставить select_related
#пример
#ar = Article.objects.select_related('author'.get(pk=1))
#для связи много ко многим нужно prefetch_related
#  надо делать через prefetch_related
#article_tags = Article.objects.prefetch_related('tags').get(id=1)

    if filtr_type == 'tag':
        news = Article.articleenable.filter(tags=filtr_val)
        context = {'filtr_type':'tag'}
    elif filtr_type == 'author':
        #news = Article.objects.all()
        news = Article.articleenable.filter(author=filtr_val)
        context = {'filtr_type': 'author'}
    elif filtr_type == 'category':
        news = Article.articleenable.filter(category=filtr_val)
        context = {'filtr_type': 'category'}
    # elif filtr_type == 'one':
    #     news = Article.articleenable.filter(id=filtr_val)
    #     context = {'filtr_type': 'one'}
    else:
        pass
        #news = Article.articleenable.all()
        #context = {'filtr_type': 'all'}
    ######  "Этот блок в 2 вьюшках singlepost  и  news_all
    context['news'] = news
    #context['tags'] = Tag.objects.filter(status=True).values('id', 'title','tag_count_m','tag_count_m2')
    #context['tags'] = Tag.objects.filter(status=True)
    context['tags'] = Tag.objects.all()
    context['categories'] = Categories.categoriesenable.all()#.values('id', 'title_cat')
    context['news_spisok_rigth'] = Article.articleenable.all().order_by('-date')[:3]
    ###

    # context = {'news': news}
    print(filtr_type, filtr_val)
    print('*******************')
    return render(request,'news/news.html', context)

def news_author(request, author_id):
    news = Article.articleenable.filter(author=author_id)
    context = {'news': news, 'author': User.objects.get(id=author_id)}
    return render(request,'news/news_author.html', context)



###
# мы написали класс миксин для внедрения подсчетпросмотров на статье
# но у меня реализация тут функция а не класс поэтому никак не сделать, может переделаю я тут записал пример как
#
#from .utils import  ViewCountMixin#
#class ArticleDetailView(ViewCountMixin, DetailView):
from .utils import ViewCountMixin_for_def, get_client_ip


# просмотр статьи полностью
def singlepost(request, id):
    news_one = Article.articleenable.get(id=id)
    # пародия на миксин
    ViewCountMixin_for_def(request,news_one)
    # пародия закончилась
    context = { 'news_one' : news_one}
    ######  "Этот блок в 2 вьюшках singlepost  и  news_all
    #context['tags'] = Tag.objects.filter(status=True).values('id', 'title')
    #context['tags'] = Tag.objects.filter(status=True)
    # context['tags'] = (Tag.objects.filter(status=True).annotate(tag_count=Count('article')).all())
    # context['categories'] = Categories.objects.filter(enable_cat=True).values('id', 'title_cat')
    context['tags'] = Tag.objects.all()
    context['categories'] = Categories.categoriesenable.all()#.values('id', 'title_cat')
    context['news_spisok_rigth'] = Article.articleenable.all().order_by('-date')[:3]
    #####
    return render(request,'news/singlepost.html', context)


# def profil(request):
#     return render(request,'news/profil.html')

def custom_404(request, exception):
    #return redirect('/')
    return HttpResponseNotFound('ОППА не куда идти наш 404')


#@login_required(login_url="/accounts/login/")
#@login_required(login_url='users:login')   # хотя какое-то избыточно наверно тк мы проверяем вхождение в группу
#@check_group('Authors')
def create_article(request):
    # проверка авторизовани или нет
    # request.user.is_authenticated:
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            new_article = form.save()
            AR = Article.articleenable.get(id = new_article.id)
            AR.author = current_user
            AR.save()
            # пример как мани ту мани сохранять
            #if current_user.id != None:
            #print(f' наш пользователь {current_user.id}')
            # # пример иот препода
            # current_user = request.user
            # if current_user.id != None:  # проверили что не аноним
            #     new_article = form.save(commit=False)
            #     new_article.author = current_user
            #     new_article.save()  # сохраняем в БД
            #     form.save_m2m()  # сохраняем теги
            # #
            for img in request.FILES.getlist('image_field'):
                Image.objects.create(article=new_article, image=img, title=img.name)

            #return redirect(f'news/singlepost/{str(new_article.id)}/' )
            #return HttpResponseRedirect(reverse('news:news_all', args=['all','0']))
            send_mail_to_admin('Статья добавлена',
                               'Статья добавлена - ' + current_user.username + '/ с адреса' + get_client_ip(
                                   request))
            #return HttpResponseRedirect(reverse('news:singlepost', args=[new_article.id]))
            return redirect(reverse('news:singlepost', args=[new_article.id]))
    else:
        form = ArticleForm()

    context = {'form': form}
    #context['tags'] = Tag.objects.filter(status=True).values('id', 'title')
    #context['tags'] = Tag.objects.filter(status=True)
    # context['tags'] = (Tag.objects.filter(status=True).annotate(tag_count=Count('article')).all())
    context['tags'] = Tag.objects.all()
    context['categories'] = Categories.categoriesenable.all()#.values('id', 'title_cat')
    context['news_spisok_rigth'] = Article.articleenable.all().order_by('-date')[:3]

    return render(request,'news/create_article.html', context)

#@check_group('Authors')
class ArticleDeleteView(LoginRequiredMixin,  DeleteView):
    login_url = 'users:login' # отправляем на авторизацию
    model = Article
    template_name = 'news/delete_news.html'
    success_url = reverse_lazy('news:news')


#@check_group('Authors')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'  # отправляем на авторизацию
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title', 'anouncement', 'text', 'enable', 'category', 'tags', 'article_image']
    #если надо передаем доп параметры
    #extra_context = {}
    extra_context = {
        #'tags': Tag.objects.filter(status=True).values('id', 'title'),
        'tags': Tag.objects.all(),
        'categories': Categories.categoriesenable.all(),
        'news_spisok_rigth': Article.articleenable.all().order_by('-date')[:3]
    }


#@check_group('Authors')
class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'  # отправляем на авторизацию
    model = Categories
    fields = ['title_cat','name_cat','user']
    #template_name = 'news/create_category.html'
    template_name = 'news/create_article.html'
    success_url = reverse_lazy('news:news')
    extra_context = {
        #'tags': Tag.objects.filter(status=True).values('id', 'title'),
        'tags': Tag.objects.all(),
        'categories': Categories.categoriesenable.all(),
        'news_spisok_rigth': Article.articleenable.all().order_by('-date')[:3]
    }


#@check_group('Authors')
class TagCreateView(LoginRequiredMixin,  CreateView):
    login_url = 'users:login'
    model = Tag
    fields = ['title']
    #template_name = 'news/create_category.html'
    template_name = 'news/create_article.html'
    success_url = reverse_lazy('news:news')
    extra_context = {
        #'tags': Tag.objects.filter(status=True).values('id', 'title'),
        'tags': Tag.objects.all(),
        'categories': Categories.categoriesenable.all(),
        'news_spisok_rigth': Article.articleenable.all().order_by('-date')[:3]
    }

    ########################
    ######################33
    ###    примеры
    #
    # у меня так работает
    #   tags_list = (Tag.objects
    #                  .annotate(num_articles=Count('article'))
    #                  .all())
    # authors_list = User.objects.annotate(Count('article'))
    # articles = (Article.objects
    #                         .select_related("author")
    #                         .prefetch_related('tags')
    #                         .annotate(Count('tags'))
    #                         .filter(category__iexact=target)
    #                         .filter(tags__in=tags_selected)
    #                         .filter(author__in=authors_selected)
    #                         .order_by('-dt_public', 'title')
    #                         .all())
    #

    # можно в моделях прикрутить поле
    # def tag_count(self):
    #     count = self.article_set.count()
    #     # комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
    #     # мы можем обращаться к связанным таблицам при помощи синтаксиса:
    #     # связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
    #     # и вызываем метод count
    #     return count


# навесим проверку авторизации
@login_required()
def test_ajax(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # берем данные которые пришли в ajax запросе
            data = json.load(request)
            print('полученные данные:')
            val1 = data['my_key1']
            print(val1)
            print('можно циклом')
            for key in data:
                 print(f'Ключ- {key}  Значение- {data[key]}')
                 #print(data[key])
            # получаем данные для отправки из БД
            users = User.objects.all()
            dict_data = {}
            # положим в словарь
            for el in users:
                #print(el.username) #print(el.pk)
                dict_data[el.pk] = el.username
            #print(dict_data)
            # добавим еще данных
            dict_data['status']='успешно'
            dict_data['tlf']= "8-911-789-12-45"
            dict_data['message'] = "Выгрузка пользователей"

            # отправим подготовленные данные
            return JsonResponse(dict_data )
        return JsonResponse({'status': 'Ошибка запроса_1'}, status=400)
    else:
        return HttpResponseBadRequest('Ошибка запроса_2')


def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #if request.is_ajax():
        q = request.GET.get('term', '')
        # вывод подстановка э то титле а поиск в зависимости от выбора радио бокса
        #articles = Article.objects.filter(Q(title__icontains=q) | Q(text__icontains=q))
        articles = Article.objects.filter(title__icontains=q,text__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
      # place_json = {}
      # place_json = pl.city + "," + pl.state
      # results.append(place_json)
        # data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
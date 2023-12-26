from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

#from . models import News


def index(request):
    #return HttpResponse("<h1> Index </h1>")
    #value = 10
    #l = ['one','two','three']
    #context = {'title1' : 'Главная страница',
    #           'header1' : 'Заголовок страницы',
    #           'value':value,
    #           'number': l}
    #n1 = News('213','12312','01.09.2023')
    #return render(request,'main/index.html', context)
    return redirect('newspage/')

#
# def news(request):
#     #return HttpResponse("<h1> Index </h1>")
#     return render(request,'main/news.html')
#
# def register(request):
#     #return HttpResponse("<h1> Index </h1>")
#     return render(request,'main/register.html')
#
# def login(request):
#     #return HttpResponse("<h1> Index </h1>")
#     return render(request,'main/login.html')
#
#
# def about(request):
#     #return HttpResponse("<h1> About</h1>")
#     return render(request, 'main/about.html')
#
# def profil(request):
#     #return HttpResponse("<h1> Contacts </h1>")
#     return render(request, 'main/profil.html')
#
# def content(request):
#     #return HttpResponse("<h1> Contacts </h1>")
#     return render(request, 'main/content.html')
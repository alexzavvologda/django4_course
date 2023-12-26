from django.core.mail import send_mass_mail
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect

from django.contrib import messages


def check_group(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            # наш пользователь текущий
            user = request.user
            # проверим если есть группы указанные у нашего пользователя
            if user.groups.filter(name__in=groups):
                # группы нашлись, то выполним декорируемую функцию
                return function(request, *args, **kwargs)
            messages.warning(request,f'Нет доступа- доступ только пользователям из групп - {groups}')
            # отправляем на ссылку откуда он пришел
            return HttpResponseRedirect(request.POST.get('next','/'))
        return wrapper
    return decorator


def send_mail_to_admin(subject, message):
    datatuple = (
        (subject, message, 'test@piloramservis.ru', ['alexzav@inbox.ru']),
        #('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
    )
    #print('Попытка отправить письмо')
    try:
        send_mass_mail(datatuple)
        print('Отправлено письмо')
    except:
        print('Ошибка отправить письмо')




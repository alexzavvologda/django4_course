

#разные утилитки для проекта новостей


# получение ip адлреса из запроса
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        if x_forwarded_for:
            ip = x_forwarded_for(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return '1.1.1.1'

from .models import ViewCount



#сделан миксин чтобы добавлять в классы как миксин но у меня не класс на просмотре одно новости,
# а процедура, поэтому я сделаю вариант как процедура  НИЖЕ
#
class ViewCountMixin:
    def get_object(self):
        # получаем обект из родительского класса
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        # если такой счетчик уже есть то ничего есдли нет то добавляем в таблицу
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj

# смотри вверх что это за пародия
def ViewCountMixin_for_def(request,article):
    # получаем обект из родительского класса
    #obj = super().get_object()
    ip_address = get_client_ip(request)
    # если такой счетчик уже есть то ничего есдли нет то добавляем в таблицу
    ViewCount.objects.get_or_create(article=article, ip_address=ip_address)
    return article

from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'gender']
    list_filter = ['user', 'nickname', 'gender']


from django.contrib.auth.models import Group
# делаем актион действие для админки перевод пользователя из группы по умолчанию в группу авторов
def make_author(modeladmin, request, queryset):
    # queryset это выборка которую мы получаем в админке из пользователей
    group = Group.objects.get(name='Authors')
    ungroup = Group.objects.get(name='Actions Required')
    # идем по польззователям которые выбраны
    for user in queryset:
        #добавим в группу автор те подтвердим
        user.groups.add(group)
        #удалим группу для временных авторов по умолчанию
        user.groups.remove(ungroup)



make_author.short_description = 'Утвердить автора'

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    actions = [make_author]

# к этому был комментарий что нужно убрат обычного юзера а поставить нашего кастомного
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['article','user','create_at']
admin.site.register(FavoriteArticle, FavoriteArticleAdmin)
from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count

# Register your models here.
from .models import *
#########
#########     настройка админки постридер 10 и 11
#########

# создаем свои фильтры для админки
class ArticleFilter(admin.SimpleListFilter):  #  ми потом добавим в молдели в список филтров
    title = 'По длине новости'
    # ключ параметр для адреснойс троки гет запрос
    parameter_name = 'text'
    # функция которая определена
    def lookups(self, request, model_admin):
        return [
            ('S',('Короткие, <100 зн. ')),
            ('M', ('Средние, 100-500  зн. ')),
            ('L', ('Длинные, >500 зн. ')),]
    def queryset(self,request, queryset):   # lt _ меньше   lte меньше равно  gt больше  gte больше равно
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500,
                                                                     text_len__gte=100)
        if self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)


##  отображение нескольких картинок в админ панели
## чтобы отобразить картинки из таблицы Image в карточке новости

# потом надо это зарегистрировать в самой модели артикле inlines = [ArticleImageInline,]
## правила наименования  в карточке какого объекта будем выводить из другой таблицы. в Article Image
class ArticleImageInline(admin.TabularInline ):
    #TabularInline  в горизонталь
    #StackedInline столбиком
    # привязываем какую модель
    model = Image
    # сколько полей ввод будет изнгачально, но если не хватит они добавятся.
    extra = 3
    # какеи поля из Image мы запретим редактировать
    readonly_fields = ('id','image_tag')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # если использовать это поле, то увидим только указанные поля в админке
    #fields = ['title','text']
    # можно по другому э то список исключаемых полей
    #exclude = ['date']
    #list_display = ['id', 'title', 'author', 'date', 'category', 'enable', 'image_tag' ,'symbols_count','symbols_count_display']
    list_display = ['id', 'title', 'author', 'date', 'category', 'enable', 'image_tag', 'symbols_count_display','image_tag_2']
    list_filter = ['id', 'title', 'author', 'date', 'category', 'enable',ArticleFilter]
    list_display_links = ('id',  'author')
    ordering = ['-id', 'author']
    # разрешение на редактирование в админке/ они не должны быть в списке редактируемых list_display_links
    list_editable = ['title']
    # запрет на редактирование
    readonly_fields = ('date',)
    # стр 19 постридер 10 предзаполненные поля
    # нужно поле слаг в модели
    #prepopulated_fields = {'slug' : ('title',)}

    # расположение выбора полей много ко многим    ///      !!!!  Вредактировании новости в АДМИНКЕ
    # когда много будет тегов мможно эти фильтры вытащить чтобы отбирать теги по фильтрам и навешивать найлденные
    #filter_vertical = ['tags'] #
    #filter_vertical['tags']


    # активировать панель поиска в админке
    # чтобы искать по связанным таблица м назв табл двойное подчеркивание назв поля
    # учитывать что ищет с учетом регистра
    #варианты - название поля и функция ['title__icontains']- без учета регистра ['title__startswith'] начинается с
    search_fields = ['title','tags__title']

    # действие с новостями в админ панели описали ниже в этой модели  № прописать ниже процедуру с декоратором @admin.action
    actions = ['action_article_enable','action_article_disable']
    # если без декоратора
    ###admin.site.register(Article, ArticleAdmin)
    # пагинация в админке
    list_per_page = 10

    inlines = [ArticleImageInline,]
    # изменение названия столбца в админке
    @admin.display(description='Буков')
    def symbols_count(self, article: Article):
        return f'Колличество символов: {len(article.text)}'

    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count_display(self, article: Article):
        return f'Кол-во символов: {len(article.text)}'
    #from django.db.models.functions import Length
    # переопределим метод получения данных берем сам кверисет и переопределяем, чтобы можно было сортировать по полю кол-во символов
    # и ето поле используем в symbols_count_display т.е тут его определили путем добавления к кверисету и можно его использовать
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset

    @admin.action(description='Активировать выбранные статьи')
    def action_article_enable(self,request, queryset):
        amount = queryset.update(enable=True)
        self.message_user(request,f'Активировано {amount} статей')

    @admin.action(description='Деактивировать выбранные статьи')
    def action_article_disable(self,request, queryset):
        amount = queryset.update(enable=False)
        self.message_user(request,f'Деактивировано {amount} статей')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'article', 'image_tag']






@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_cat', 'name_cat', 'date_cat', 'user',  'enable_cat']
    list_filter = ['id', 'title_cat', 'name_cat', 'date_cat', 'user', 'enable_cat']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']

# подробнее описано в Article вверху
    @admin.display(description='Использование', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset

# модель зарегили чтобы в админке видеть таблицы с просмотрами
@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ['article', 'ip_address', 'view_date']
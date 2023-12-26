from django.db import models
import datetime
from django.contrib.auth.models import User

from django.db.models.functions import Length
from django.db.models import Count

from django.utils.safestring import mark_safe


# Create your models here.


class Tag (models.Model):
    title = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title+''

    #@admin.display(description='Использование', ordering='tag_count')
    def tag_count(self):
        # не работает или надо разобраться  count = self.objects.annotate(tag_count=Count('article'))
        count = self.article_set.count()
        #print(count)
        #комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
        #мы можем обращаться к связанным таблицам при помощи синтаксиса:
        #связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
        #и вызываем метод count
        return count
    class Meta:
        ordering = ['status', 'title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'



class ArticleEnable(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enable=True)  # enable=True / author='alexzav'
        # return super().get_queryset().filter(author="Roald Dahl")

class CategoriesEnable(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enable_cat=True)  # enable=True / author='alexzav'
        # return super().get_queryset().filter(author="Roald Dahl")

# class DahlBookManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(author="Roald Dahl")

class Categories(models.Model):
    objects = models.Manager()
    categoriesenable = CategoriesEnable()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    title_cat = models.CharField('Кор. назв.', max_length=20, null=False, unique=True)
    name_cat = models.CharField('Категория Наим.', max_length=50)
    enable_cat = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,default=User)
    date_cat = models.DateTimeField('Дата ввода категории', auto_now=True)
    def __str__(self):
        #return f'Категория {self.title_cat} / {self.name_cat}'
        return f'Категория {self.title_cat} '

    def cat_count(self):
        # не работает или надо разобраться  count = self.objects.annotate(tag_count=Count('article'))
        count = self.article_set.count()
        #комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
        #мы можем обращаться к связанным таблицам при помощи синтаксиса:
        #связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
        #и вызываем метод count
        return count

class Article(models.Model):
    objects = models.Manager()
    articleenable = ArticleEnable()
    class Meta:
        ordering = ['title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    author = models.ForeignKey(User, on_delete=models.Prefetch, null=True, default=User)
    title = models.CharField('Название', max_length=150, default='')
    anouncement = models.TextField('Аннотация', max_length=350)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now=True)
    enable = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True )
    tags = models.ManyToManyField(to=Tag, blank=True)
    article_image = models.ImageField(blank=True, default='default_news.jpg', upload_to='article_images')

    #image_field =
    # поле для слаг  в админке должно быть
    # slug = models.SlugField(default='', null= True, blank=True)

    def image_tag(self):
        if self.article_image is not None:
            return mark_safe(f'<img src="{self.article_image.url}" height="50"/>')

    def image_tag_2(self):
        image = Image.objects.filter(article=self)
        #print('!!!!',image)
        if image:
            return mark_safe(f'<img src="{image[0].image.url}" height="50px" width="auto" />')
        else:
            return '(no image)'
    def __str__(self):
        return f'Новость: {self.title}. Дата создания: {self.date} '

    def text_short(self):
        return f' {self.text [:500]} ...'

    def get_absolute_url(self):
        return f'/newspage/singlepost/{self.id}'
    # а можно и по  return f'/news/singlepost/{self.pk}'

    # добавим метод чтобы с новостью получать кол-во просмотров
    # views - это поле в модели просмотров
    def get_views(self):
        return self.views.count()


    # def get_absolute_url_author(self):
    #     return f'/newspage/news_author/{self.author.id}'
    #     # а можно и по  return f'/news/singlepost/{self.pk}'

    # def get_absolute_url_all(self):
    #     return f'/newspage/news_all/all/0'
    #     # а можно и по  return f'/news/singlepost/{self.pk}'

    # дополнительное поле и добавить в список выводимых полей

    # def symbols_count(self):
    #     return f'Колличество символов: {len(self.text)}'
    # можно и в админке описать
    # изменение названия столбца в админке
    #@admin.display(description='Буков')
    # def symbols_count(self, article: Article):
    #     return f'Колличество символов: {len(article.text)}'




class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='article_many_images/') #лучше добавить поле default !!!

    def __str__(self):
        return self.title
    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto" />')
        else:
            return '(no image)'


class ViewCount(models.Model):
    #related_name - это имя через которое мы можем обращаться из новости к счетчику просмотра
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views' )
    ip_address = models.GenericIPAddressField()
    #auto_now_add = True время при добавлении записи поставить ся текущее
    view_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-view_date',)
        indexes = [models.Index(fields=['-view_date'])]

    def __str__(self):
        return self.article.title


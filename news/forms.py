from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple,  ModelChoiceField

from .validators import russian_email
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Article, Categories


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self,*args,**kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data,(list,tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    email = forms.EmailField(validators=[MaxLengthValidator(20), russian_email])
    message = forms.CharField(
        widget=forms.Textarea
        #,
        #help_text='Описание поля',
        #required=True, # обязательное не обязательное
        #label='метка',
        #initial='121212',
        #error_messages='Ошибка текст',
        ##validators=[ma],
        #disabled=False
    )



class ArticleForm(ModelForm):
    image_field = MultipleFileField()
    class Meta:
        model = Article
        fields = ['title','anouncement','text','tags','category', 'article_image','image_field']
        widgets = {
            'anouncement' : Textarea(attrs={'cols':80, 'rows':2}),
            'tags' : CheckboxSelectMultiple()#,
           # 'category' :   ModelChoiceField(queryset=Categories.objects.all(), empty_label=None, to_field_name="pk")
        }





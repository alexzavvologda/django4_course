from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple,  ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator,  MaxLengthValidator

from django.core.validators import MinLengthValidator, MaxLengthValidator
from . models import User



class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, min_length=5, label='Пользователь' , widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# все делается
# CreateUserView
# class RegisterForm(forms.Form):
    #login = forms.CharField(max_length=30, min_length=5, label='Пользователь')
    #password = forms.PasswordInput()
    # password = forms.PasswordInput()
    #password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput())
    #email = forms.EmailField(label='Email')
    #email = forms.EmailField(label='Email')
    # pass

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'})  , validators=[MinLengthValidator(5)])
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}),
                               validators=[MinLengthValidator(3)])
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}),
                               validators=[MinLengthValidator(3)])

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}) )
    password2 = forms.CharField(label='Пароль повтор', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


    class Meta:
        model = User
        #model = get_user_model()
        fields = ['username', 'email', 'first_name','last_name', 'password1','password2']
        labels = {
            'email' : 'E-mail',
            'first_name' :'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }







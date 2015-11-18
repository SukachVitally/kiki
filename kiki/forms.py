from django import forms
from kiki import models


class RegistrationForm(forms.Form):

    username = forms.CharField(label='Login', max_length=50, min_length=2)
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)


class ArticleForm(forms.Form):

    name = forms.CharField(max_length=100)
    text = forms.CharField()
    category = forms.ChoiceField(models.Article.CATEGORIES)



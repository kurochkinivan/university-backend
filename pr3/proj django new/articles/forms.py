from django import forms
from django.forms import ModelForm
from .models import Article
from django_ckeditor_5.widgets import CKEditor5Widget


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields =  ['name', 'content', 'excerpt', 'featured_image', 'tags', 'category']
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name='extends'
            ),
            'tags': forms.CheckboxSelectMultiple(),
            'category': forms.Select()
        }

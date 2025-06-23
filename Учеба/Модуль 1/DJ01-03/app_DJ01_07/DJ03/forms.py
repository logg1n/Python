from django.forms import ModelForm, TextInput, Textarea
from .models import NewsPost

class NewsForm(ModelForm):  # Исправлено: ModelForm вместо ModelForms
    class Meta:
        model = NewsPost
        fields = ['title', 'user', 'short_description', 'text']
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'id': "title",
                'maxlength': "50",
                'required': True
            }),
            'user': TextInput(attrs={
                'class': "form-control",
                'maxlength': "25",
                'required': True
            }),
            'short_description': TextInput(attrs={
                'class': "form-control",
                'maxlength': "200",
                'required': True
            }),
            'text': Textarea(attrs={
                'class': "form-control",
                'rows': 7,
                'required': True
            }),
        }
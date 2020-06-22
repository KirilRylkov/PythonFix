from .models import News
from django.forms import ModelForm, TextInput


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['search']
        widgets = {'search': TextInput(attrs={'class': 'form=control', 'id': 'search', 'placeholder': 'Поиск'})}

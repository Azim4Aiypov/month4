from django import forms
from posts.models import Post

class PostForm(forms.Form):
    image = forms.ImageField(required=False)
    title = forms.CharField(max_length=256)
    content = forms.CharField(max_length=512)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        print(title)
        content = cleaned_data.get("content")
        print(content)
        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError("Title and content cannot be the same.")
        return cleaned_data
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and title.lower() == "javascript":
            raise forms.ValidationError("Javascript is not allowed, it's a reserved word.")
        return title
    
class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'content']  

class PostBaseForm(forms.Form):
    title = forms.CharField(label="Заголовок поста", max_length=200, 
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}))
    content = forms.CharField(label="Содержание", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    image = forms.ImageField(label="Изображение", required=False) # required=False, так как изображение может быть необязательным  

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post # Указываем модель, к которой привязана форма
        fields = ['title', 'content', 'image'] # Указываем, какие поля из модели использовать
        # Или можно использовать 'exclude = ['created_at', 'updated_at']' для исключения полей
        widgets = { # Необязательно, но полезно для настройки HTML-атрибутов
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
        }
        labels = { # Необязательно, для кастомных лейблов
            'title': 'Название поста',
            'content': 'Текст поста',
            'image': 'Выберите изображение',
        }
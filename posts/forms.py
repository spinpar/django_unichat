from django import forms
from .models import Post,Comment, Reply, Event

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="",
        required=False
    )
    image = forms.ImageField(
        label="Adicionar foto",
        required=False
    )

    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escreva um comentário...'}),
        label="",
    )

    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escreva uma resposta...'}),
        label="",
    )

    class Meta:
        model = Reply
        fields = ['content']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'event_time', 'image']

        labels = {
            'title': 'Título do Evento',
            'description': 'Descrição',
            'location': 'Local do Evento',
            'event_date': 'Data do Evento',
            'event_time': 'Hora do Evento',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Evento'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva o evento...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do Evento'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

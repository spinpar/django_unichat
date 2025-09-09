from django import forms
from .models import Post,Comment, Reply

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
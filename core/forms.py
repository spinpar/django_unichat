from django import forms
from posts.models import Post, Event
import re

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not re.match(r'^[A-Za-z0-9]+$', title):
            raise forms.ValidationError("Use apenas letras e números no título.")
        return title


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'event_time']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not re.match(r'^[A-Za-z0-9]+$', title):
            raise forms.ValidationError("Use apenas letras e números no título.")
        return title

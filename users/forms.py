from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Course
from datetime import date
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple


## User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'Email'})
    )
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)
    date_of_birth = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    avatar = forms.ImageField(
        label="Avatar de perfil",
        required=False
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Curso",
        empty_label="Selecione seu curso",
        required=True
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'date_of_birth', 'avatar', 'course')
        labels = {
            'username': 'Nome de usuário',
        }
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("Você deve ter 18 anos ou mais para se registrar.")
        return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse email já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()

            avatar = self.cleaned_data.get('avatar', None)
            date_of_birth = self.cleaned_data.get('date_of_birth', None)
            course = self.cleaned_data.get('course', None)

            profile = Profile.objects.create(
                user=user,
                avatar=avatar,
                date_of_birth=date_of_birth,
            )
            
            if course:
                profile.course.add(course)
                
        return user
    

## Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    course = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label="Cursos"
    )

    def __init__(self, *args, **kwargs):
        # Remove o argumento 'is_teacher' antes de chamar o método pai
        is_teacher = kwargs.pop('is_teacher', False)
        super().__init__(*args, **kwargs)

        # Se o usuário NÃO for um professor, remove o campo 'is_teacher'
        if not is_teacher:
            del self.fields['is_teacher']

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'website', 'avatar', 'course', 'is_teacher']
        labels = {
            'bio': 'Bio',
            'location': 'Localização',
            'website': 'Site',
            'avatar': 'Foto de Perfil',
            'is_teacher': 'Sou um(a) professor(a)'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}), }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }
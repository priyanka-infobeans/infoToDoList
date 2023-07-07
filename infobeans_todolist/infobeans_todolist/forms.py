from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'profile_photo', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_photo'].required = False
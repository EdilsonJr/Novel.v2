from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        models = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    class Meta:
        models = User
        fields = ('first_name', 'username', 'password', 'email')

        def clean(self, *args, **kwargs):
            data = self.data
            cleaned = self.cleaned_data


from django import forms
from .models import User, Person, Project


class UserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Person.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:  # НИЖЕ МАГИЯ
        model = User
        fields = ['login', 'password', 'user']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserDeleteForm(forms.Form):
    id_user_id = forms.IntegerField(label='ID пользователя',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['id_project', 'Title', 'curator_project', 'deadline']
        widgets = {
            'id_project': forms.NumberInput(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'curator_project': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class ProjectFormDeleteForm(forms.Form):
    id_project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

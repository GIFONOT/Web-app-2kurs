from django import forms
from .models import User, Person, Project, Project_person


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
        fields = ['Title', 'Title', 'curator_project', 'deadline']
        widgets = {
            'Title': forms.NumberInput(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'curator_project': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class ProjectFormDeleteForm(forms.Form):
    id_project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))


class ProjectPersonForm(forms.ModelForm):
    id_person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    id_project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Project_person
        fields = ['id_person', 'id_project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_person'].label_from_instance = lambda obj: f'{obj.Name} {obj.Surname} {obj.Middle_name}'
        self.fields['id_project'].label_from_instance = lambda obj: obj.Title



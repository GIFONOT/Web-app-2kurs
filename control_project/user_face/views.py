from django.shortcuts import render, redirect
from .forms import UserForm, UserDeleteForm, ProjectForm, ProjectFormDeleteForm, ProjectPersonForm
from .models import Person, User, Project, Project_person


def add_main_user(request):
    return render(request, 'user_face/add_main_user.html')


def add_project_person(request):
    if request.method == 'POST':
        form = ProjectPersonForm(request.POST)
        if form.is_valid():
            form.save()
            # Дополнительные действия после успешного сохранения формы
    else:
        form = ProjectPersonForm()
    project_persons = Project_person.objects.all()
    return render(request, 'user_face/add_project_person.html', {'form': form, 'project_persons': project_persons})


def add_project(request):
    form1 = ProjectForm()
    form2 = ProjectFormDeleteForm()

    if request.method == 'POST':
        if 'form1_submit' in request.POST:
            form1 = ProjectForm(request.POST)
            if form1.is_valid():
                form1.save()
                return redirect(request.path)

        if 'form2_submit' in request.POST:
            form2 = ProjectFormDeleteForm(request.POST)
            if form2.is_valid():
                id_project = form2.cleaned_data['Title']
                try:
                    string_representation = str(id_project)
                    value = string_representation.replace('<Project: ', '').rstrip('>')
                    project = Project.objects.get(id_project=value)
                    project.delete()
                    return redirect(request.path)
                except User.DoesNotExist:
                    form2.add_error('Title', 'Проект с указанным ID не найден')
    else:
        from1 = ProjectForm()
        form2 = ProjectFormDeleteForm()

    existing_projects = Project.objects.all()
    return render(request, 'user_face/add_project.html',
                  {'form1': form1, 'form2': form2, 'existing_projects': existing_projects})


def add_user(request):
    form1 = UserForm()
    form2 = UserDeleteForm()

    if request.method == 'POST':
        if 'form1_submit' in request.POST:
            form1 = UserForm(request.POST)
            if form1.is_valid():
                login = form1.cleaned_data.get('login')
                try:
                    User.objects.get(login=login)
                    form1.add_error('login', 'Пользователь с таким логином уже существует')
                except User.DoesNotExist:
                    form1.save()
                    return redirect(request.path)

        if 'form2_submit' in request.POST:
            form2 = UserDeleteForm(request.POST)
            if form2.is_valid():
                id_user_id = form2.cleaned_data['id_user_id']
                try:
                    user = User.objects.get(user=id_user_id)
                    user.delete()
                    return redirect(request.path)
                except User.DoesNotExist:
                    form2.add_error('id_user_id', 'Пользователь с указанным ID не найден')

    else:
        form1 = UserForm()
        form2 = UserDeleteForm()

    existing_users = User.objects.all()  # Получение списка уже существующих пользователей
    return render(request, 'user_face/add_user.html',
                  {'form1': form1, 'form2': form2, 'existing_users': existing_users, 'persons': Person.objects.all()})

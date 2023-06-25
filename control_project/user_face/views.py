from datetime import date
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from .forms import UserForm, UserDeleteForm, ProjectForm, ProjectFormDeleteForm, ProjectPersonForm, \
    ProjectPersonDeleteForm
from .models import Person, User, Project, Project_person


def generate_report(request):
    # Получите данные для отчета
    projects = Project_person.objects.filter(status='completed')
    user_id = request.session.get('id')
    person = Person.objects.get(id_person=user_id)

    # Создайте временный файл для сохранения PDF-документа
    temp_file = '/Users/andrejsmirnov/PycharmProjects/web-app-2kurs/file.pdf'

    # Создайте PDF-документ
    p = canvas.Canvas(temp_file, pagesize=letter)

    # Добавьте информацию о сотруднике
    p.drawString(100, 700, f"Employee: {person.Name} {person.Surname} {person.Middle_name}")

    # Добавьте информацию о проектах
    y = 650
    for project in projects:
        p.drawString(100, y, f"Project: {project.id_project.Title}")
        # Добавьте другую информацию о проекте...

        y -= 20  # Переместитесь на следующую строку

    p.showPage()
    p.save()

    # Откройте временный файл и прочитайте его содержимое
    with open(temp_file, 'rb') as file:
        pdf_data = file.read()

    # Удалите временный файл
    # ...

    # Отправьте файл отчета в ответе HTTP
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response


def save_status(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        status = request.POST.get('status')

        # Находим связь Project_person по идентификаторам персоны и проекта
        project_person = Project_person.objects.get(id_person=request.session['id'], id_project=project_id)

        # Сохраняем новый статус в связи Project_person
        project_person.status = status
        project_person.save()

    return redirect('user_check')


def user_check(request):
    user_id = request.session.get('id')
    project_persons = Project_person.objects.filter(id_person=user_id)
    projects = []
    today = date.today()

    # Создаем список проектов с дополнительными данными о времени до дедлайна
    for project_person in project_persons:
        project = project_person.id_project
        deadline = project.deadline
        remaining_days = (deadline - today).days

        project_data = {
            'id': project.id_project,
            'title': project.Title,
            'curator': project.curator_project,
            'deadline': deadline,
            'remaining_days': remaining_days,
            'status': project_person.status,
        }

        projects.append(project_data)

    return render(request, 'user_face/user_check.html', {'projects': projects})


def add_main_user(request):
    return render(request, 'user_face/add_main_user.html')


def add_project_person(request):
    form1 = ProjectPersonForm()
    form2 = ProjectPersonDeleteForm()
    if request.method == 'POST':
        if 'form1_submit' in request.POST:
            form1 = ProjectPersonForm(request.POST)
            if form1.is_valid():
                form1.save()
                return redirect(request.path)
                # Дополнительные действия после успешного сохранения формы
        if 'form2_submit' in request.POST:
            form2 = ProjectPersonDeleteForm(request.POST)
            if form2.is_valid():
                Id = form2.cleaned_data['ID']
                string_representation = str(Id)
                value = int(string_representation.split('(')[1].split(')')[0])

                proj = Project_person.objects.get(ID=value)
                proj.delete()
                return redirect(request.path)

    else:
        form1 = ProjectPersonForm()
        form2 = ProjectPersonDeleteForm()

    project_persons = Project_person.objects.all()
    return render(request, 'user_face/add_project_person.html',
                  {'form1': form1, 'form2': form2, 'project_persons': project_persons})


def add_project(request):
    form1 = ProjectForm()
    form2 = ProjectFormDeleteForm()

    if request.method == 'POST':
        if 'form1_submit' in request.POST:
            form1 = ProjectForm(request.POST)
            if form1.is_valid():
                id_project = form1.cleaned_data['id_project']
                try:
                    project = Project.objects.get(id_project=id_project)
                    project.Title = form1.cleaned_data['Title']
                    project.curator_project = form1.cleaned_data['curator_project']
                    project.deadline = form1.cleaned_data['deadline']
                    project.save()
                    # Объект успешно обновлен
                except Project.DoesNotExist:
                    form1.save()

                return redirect(request.path)

        if 'form2_submit' in request.POST:
            form2 = ProjectFormDeleteForm(request.POST)
            if form2.is_valid():
                id_project = form2.cleaned_data['id_project']
                try:
                    string_representation = str(id_project)
                    value = string_representation.replace('<Project: ', '').rstrip('>')
                    project = Project.objects.get(id_project=value)
                    project.delete()
                    return redirect(request.path)
                except User.DoesNotExist:
                    form2.add_error('Title', 'Проект с указанным ID не найден')
    else:
        form1 = ProjectForm()
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

from django.db import models


class Person(models.Model):
    Name = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100)
    id_person = models.CharField(primary_key=True, max_length=6)

    # Добавьте другие поля, если они присутствуют

    class Meta:
        db_table = 'Person'

    def __str__(self):
        return str(self.id_person)


class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)

    # Добавьте другие поля, если они присутствуют

    class Meta:
        db_table = 'register_user'

    def __str__(self):
        return str(self.user)


class Project(models.Model):
    id_project = models.IntegerField(max_length=100, primary_key=True)
    Title = models.CharField(max_length=100)
    curator_project = models.CharField(max_length=100)
    deadline = models.DateField()

    class Meta:
        db_table = 'project'

    def __str__(self):
        return str(self.id_project)


class Project_person(models.Model):
    id_person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    id_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    STATUS_CHOICES = (
        ('not_started', 'Работа не начата'),
        ('in_progress', 'Работа выполняется'),
        ('completed', 'Работа выполнена'),
    )
    ID = models.IntegerField(primary_key=True, max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    class Meta:
        db_table = 'project_person'



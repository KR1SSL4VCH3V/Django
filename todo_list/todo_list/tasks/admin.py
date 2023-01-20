from django.contrib import admin


from django.contrib import admin

from todo_list.tasks.models import Task


@admin.register(Task)
class AdminToDoList(admin.ModelAdmin):
    pass


from django.contrib import admin

from to_do_app.tasks.models import Task


@admin.register(Task)
class AdminToDoList(admin.ModelAdmin):
    pass


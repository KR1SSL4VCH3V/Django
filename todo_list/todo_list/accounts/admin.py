from django.contrib import admin

from todo_list.accounts.models import Profile


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    pass

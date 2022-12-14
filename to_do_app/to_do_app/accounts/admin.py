from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    ordering = ('username', 'email',)
    list_display = ['email', 'date_joined', 'last_login', ]
    list_filter = ()

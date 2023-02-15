from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Categories, Blog


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal', {'fields': ('first_name','last_name','picture','email','address','type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date']

admin.site.register(Categories, CategoriesAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']

admin.site.register(Blog, BlogAdmin)
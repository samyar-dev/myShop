from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser, Address
from . forms import ShopUserCreationForm, ShopUserChangeForm

# Register your models here.

# class AddressInline(admin.TabularInline):
#     model = Address
#     extra = 0
    
@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    model = ShopUser
    ordering = ['phone']
    form = ShopUserChangeForm
    add_form = ShopUserCreationForm
    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active']
    # inlines = [AddressInline]

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_join', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_join', 'last_login')}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['province', 'city']
    search_fields = ['city', 'province']
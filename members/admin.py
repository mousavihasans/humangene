from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\'../password/\'>this form</a>."))

    class Meta:
        model = Member
        fields = ('email', 'password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@register(Member)
class MemberAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'date_joined')
    list_filter = ('date_joined', 'is_staff', 'is_superuser', 'is_active')

    readonly_fields = ('email', 'auth_token')
    search_fields = ('email',)
    ordering = ('-id',)

    def auth_token(self, member):
        return str(member.auth_token)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return tuple()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                (None, {
                    'classes': ('wide',),
                    'fields': ('email', 'password1', 'password2')}
                 ),
            )

        if request.user.is_superuser:
            return (
                (None, {'fields': (
                'email', 'password', 'auth_token')}),
                ('Personal info', {'fields': ('first_name', 'last_name')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                            'groups', 'user_permissions')}),
                ('Important dates', {'fields': ('date_joined',)}),
            )

        if request.user.is_staff:
            return (
                (None, {'fields': ('email',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
            )

        return ()

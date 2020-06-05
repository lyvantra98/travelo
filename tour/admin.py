from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.conf import settings

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CustomUserAdmin(UserAdmin):
  inlines = (ProfileInline, )
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')
  list_select_related = ('profile', )

  def get_phone_number(self, instance):
      return instance.profile.phone_number
  get_phone_number.short_description = 'phone'

  def get_inline_instances(self, request, obj=None):
      if not obj:
          return list()
      return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

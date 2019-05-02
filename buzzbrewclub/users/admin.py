from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.messages import ERROR

from .forms import UserChangeForm, UserCreationForm
from .tasks import merge_users_posts_threads

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name", "username"]
    actions = ['merge_users']

    def merge_users(self, request, queryset):
        if queryset.count() != 2:
            self.message_user(
                request, "Exactly two users must be selected.", level=ERROR)
            return
        final = queryset.exclude(username__startswith='_').first()
        other = queryset.filter(username__startswith='_').first()
        if not final or not other:
            self.message_user(
                request, "Exactly one user must start with _.", level=ERROR)
            return
        merge_users_posts_threads(final=final, other=other)
        self.message_user(
            request,
            f"Posts and topics moved over. {other.username} can be deleted.")

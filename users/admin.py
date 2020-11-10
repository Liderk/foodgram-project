from django.contrib import admin
from users.models import Follow


@admin.register(Follow)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    empty_value_display = 'None'

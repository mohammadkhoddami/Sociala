from django.contrib import admin
from .models import Relation
# Register your models here.

@admin.register(Relation)
class PostAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created')
    search_fields = ('from_user', 'to_user',)
    list_filter = ('created', )
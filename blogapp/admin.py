from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blogapp.models import Post, CustomUser, Comment
from blogapp.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status', 'categories']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
    search_fields = ["username", "first_name", "last_name", "email"]
    fieldsets = UserAdmin.fieldsets + ((None, { "fields": ("name",)}),)
    add_fieldsets =  UserAdmin.add_fieldsets + ((None, { "fields": ("username",)}),)
      
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','created',"active"]
    list_filter = ["active","updated","created"]
    search_fields = ["name","email","body"]
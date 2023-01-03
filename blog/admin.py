from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import BlogPost, CommentPost, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

class CommentInline(admin.StackedInline):
    model = CommentPost
    raw_id_fields = ["post"]
    # fields = ["commentor", "body", "comment_date"]
    
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "subtitle", "author__first_name", "author__last_name", "author__username", "category", "body"]
    list_display = ["title", "author", "category", "date"]
    list_filter = ["author", "category", "date"]
    inlines = [CommentInline]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "commentor", "comment_date"]
    
# Register your models here.
admin.site.unregister(Group)
admin.site.register(BlogPost, PostAdmin)
admin.site.register(CommentPost, CommentAdmin)
admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)

# @admin.register(UserProfile)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'username', 'email', 'pfp', 'bio')
    
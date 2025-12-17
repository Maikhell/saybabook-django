from django.contrib import admin
from.models import Author, Category, Genre, Book, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(UserProfile)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


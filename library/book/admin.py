from django.contrib import admin
from .models import Book, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'publication_date')
    list_filter = (
        'title',
        'author',
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'birthday')
    list_filter = (
        'first_name',
        'last_name',
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)

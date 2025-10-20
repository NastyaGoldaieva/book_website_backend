from django.contrib import admin
from .models import Book, Author, Publisher, Genre, Order, OrderItem, UserProfile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock', 'genre']
    list_filter = ['genre', 'publisher', 'author']
    search_fields = ['title', 'author__name', 'publisher__name']
    list_editable = ['price', 'stock']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count']
    search_fields = ['name']

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = 'Кількість книг'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count']
    search_fields = ['name']

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = 'Кількість книг'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count']

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = 'Кількість книг'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username']


from django.contrib import admin

# Register your models here.

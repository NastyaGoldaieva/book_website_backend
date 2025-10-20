from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Author, Publisher, Genre, Order, OrderItem, UserProfile


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = '__all__'

    def get_book_count(self, obj):
        return obj.books.count()


class PublisherSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = '__all__'

    def get_book_count(self, obj):
        return obj.books.count()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
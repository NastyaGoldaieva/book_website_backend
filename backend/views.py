from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Book, Author, Publisher, Genre, Order, OrderItem, UserProfile
from .serializers import *


class BookList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        # Фільтрація
        title = request.GET.get('title')
        author = request.GET.get('author')
        publisher = request.GET.get('publisher')
        genre = request.GET.get('genre')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__name__icontains=author)
        if publisher:
            books = books.filter(publisher__name__icontains=publisher)
        if genre:
            books = books.filter(genre__name__icontains=genre)
        if min_price:
            books = books.filter(price__gte=min_price)
        if max_price:
            books = books.filter(price__lte=max_price)

        # Сортування
        sort = request.GET.get('sort', 'title')
        if sort == 'price_asc':
            books = books.order_by('price')
        elif sort == 'price_desc':
            books = books.order_by('-price')
        elif sort == 'author':
            books = books.order_by('author__name')
        elif sort == 'publisher':
            books = books.order_by('publisher__name')
        elif sort == 'genre':
            books = books.order_by('genre__name')
        elif sort == 'newest':
            books = books.order_by('-publication_date')
        else:  # default sort by title
            books = books.order_by('title')

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value


class AuthorList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class AuthorDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            books = Book.objects.filter(author=author)
            author_serializer = AuthorSerializer(author)
            books_serializer = BookSerializer(books, many=True)

            return Response({
                'author': author_serializer.data,
                'books': books_serializer.data
            })
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PublisherList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)


class PublisherDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            publisher = Publisher.objects.get(pk=pk)
            books = Book.objects.filter(publisher=publisher)
            publisher_serializer = PublisherSerializer(publisher)
            books_serializer = BookSerializer(books, many=True)

            return Response({
                'publisher': publisher_serializer.data,
                'books': books_serializer.data
            })
        except Publisher.DoesNotExist:
            return Response({'error': 'Publisher not found'}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        user = request.user

        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()

        profile.phone = request.data.get('phone', profile.phone)
        profile.address = request.data.get('address', profile.address)
        profile.save()

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            total_amount = 0

            for item in request.data.get('items', []):
                book = Book.objects.get(pk=item['book_id'])
                quantity = item['quantity']

                if book.stock < quantity:
                    return Response(
                        {'error': f'Not enough stock for {book.title}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=quantity,
                    price=book.price
                )

                total_amount += book.price * quantity
                book.stock -= quantity
                book.save()

            order.total_amount = total_amount
            order.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class GenreDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist:
            return Response({'error': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)


class AboutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        about_info = {
            "name": "Bookstore",
            "contact": {
                "email": "contact@bookstore.com",
                "phone": "+1234567890",
                "address": "123 Main St, Kyiv, Ukraine"
            },
            "delivery_info": "We deliver worldwide within 5-7 business days.",
            "return_policy": "You can return any book within 30 days of purchase."
        }
        return Response(about_info)
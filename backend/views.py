from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book, Author, Publisher
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer


class BookList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()

        filters = {
            'title': 'title__icontains',
            'author': 'author__name__icontains',
            'publisher': 'publisher__name__icontains',
        }

        for param, filter_field in filters.items():
            value = request.GET.get(param)
            if value:
                books = books.filter(**{filter_field: value})

        sort = request.GET.get('sort', 'title')
        sort_map = {
            'price_asc': 'price', 'price_desc': '-price',
            'author': 'author__name', 'publisher': 'publisher__name',
            'newest': '-publication_date'
        }
        books = books.order_by(sort_map.get(sort, 'title'))

        return Response(BookSerializer(books, many=True).data)


class BookDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class AuthorList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(AuthorSerializer(Author.objects.all(), many=True).data)


class AuthorDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            return Response({
                'author': AuthorSerializer(author).data,
                'books': BookSerializer(author.books.all(), many=True).data
            })
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)


class PublisherList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(PublisherSerializer(Publisher.objects.all(), many=True).data)


class PublisherDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        try:
            publisher = Publisher.objects.get(pk=pk)
            return Response({
                'publisher': PublisherSerializer(publisher).data,
                'books': BookSerializer(publisher.books.all(), many=True).data
            })
        except Publisher.DoesNotExist:
            return Response({'error': 'Publisher not found'}, status=status.HTTP_404_NOT_FOUND)


class AboutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"name": "Bookstore", "status": "API is working"})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)
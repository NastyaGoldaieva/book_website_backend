from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('authors/', views.AuthorList.as_view()),
    path('authors/<int:pk>/', views.AuthorDetail.as_view()),
    path('publishers/', views.PublisherList.as_view()),
    path('publishers/<int:pk>/', views.PublisherDetail.as_view()),
    path('about/', views.AboutView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
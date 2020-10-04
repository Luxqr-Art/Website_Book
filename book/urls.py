from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookView.as_view()),
    path('filter/', views.FilterBookView.as_view(), name='filters'),
    path('<slug:slug>/', views.BookDetailVies.as_view(), name='book_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('author/<str:slug>/', views.AuthorView.as_view(), name='author_detail'),
    path('publush/<str:slug>/', views.PublushHouseView.as_view(), name='publush_house_detail'),
]

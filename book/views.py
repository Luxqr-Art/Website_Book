from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.views.generic.base import View
from .models import *
from .forms import *



class GenreYear:
    """
    Жанры и года выхода книг
    """
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Book.objects.filter(draft=False).values('year')


class BookView(GenreYear, ListView):
    """Список книг"""

    model = Book
    queryset = Book.objects.filter(draft=False)
    # template_name = 'book/book_list.html'
# джанго сам подстовляет наш html главное чтоб имя папки совпадало с именем модели
# так как наша модель называться Book и шаблон сформулирует book/book_list


class BookDetailVies(GenreYear, DetailView):
    """Полное описание книги"""

    model = Book
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return  context

# это  первый вариат передачи в базу отзывов
# class AddReview(View):
#     """Отзывы"""
#
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.book_id = pk
#             form.save()
#         return  redirect('/')


# это втророй  вариат передачи в базу отзывов  через объект
class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.book = book
            form.save()
        return  redirect(book.get_adsolute_url())


class AuthorView(GenreYear, DetailView):
    """Вывод информации о авторе"""

    model = Author
    template_name = 'book/author.html'
    slug_field = 'name'

class PublushHouseView(GenreYear, DetailView):
    """Вывод информации о издетельском доме"""

    model = PublishingHouse
    template_name = 'book/publush_house.html'
    slug_field = 'name'


class FilterBookView(GenreYear, ListView):
    """
    Фильтр фильмов
    """
    def get_queryset(self):
        """
        Q, | - или мы фильтруем по годам или по жанрам или все месте
        """

        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        )

        return queryset

class JsonFilterBooksView(ListView):
    """
    Фильты для книг Json
    """
    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'books': queryset}, safe=False)

class AddStarRating(View):
    """
    Добавление рейтинга фильму
    """
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                book_id=int(request.POST.get("book")),
                defaults={'rating_star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
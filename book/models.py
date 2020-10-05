from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""

    class Meta:
        db_table = 'Categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True, verbose_name='url')

    def __str__(self):
        return self.title


class Author(models.Model):
    """Авторы"""

    class Meta:
        db_table = 'Authors'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='authors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.name})


class Genre(models.Model):
    """Жанры"""

    class Meta:
        db_table = 'Genres'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    title = models.CharField('Жанр', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True, verbose_name='url')

    def __str__(self):
        return self.title


class PublishingHouse(models.Model):
    """Издательский дом"""

    class Meta:
        db_table = "Publishing_Houses"
        verbose_name = 'publishing house'
        verbose_name_plural = 'publishing houses'

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True, verbose_name='url')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('publush_house_detail', kwargs={'slug': self.name})

class Book(models.Model):
    """Книги"""

    class Meta:
        db_table = 'Book'
        verbose_name = 'book'
        verbose_name_plural = 'book'

    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='book/')
    year = models.PositiveSmallIntegerField('Год написание', default=2019)
    country = models.CharField('Стана', max_length=100)
    publishing_house = models.ManyToManyField(PublishingHouse, verbose_name='Издательский дом', related_name='book_publishinghouse')
    author = models.ManyToManyField(Author, verbose_name='Автор', related_name='book_author')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', related_name='book_genre')
    edition = models.PositiveIntegerField('Тираж', default=0, help_text='Указать тираж выпушенных экземпляров')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True, verbose_name='url')
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_adsolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.url})


class BookShots(models.Model):
    """Страницы из книги"""

    class Meta:
        db_table = 'Book_Shots'
        verbose_name = 'book shot'
        verbose_name_plural = 'book shots'

    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='book_shots/')
    book = models.ForeignKey(Book, verbose_name='Книги', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    """Рейтинг звезда"""

    class Meta:
        db_table = 'Rating_Star'
        verbose_name = 'rating star'
        verbose_name_plural = 'rating stars'
        ordering = ['-value']

    value = models.SmallIntegerField('Рейтинг', default=0)

    def __str__(self):
        return str(self.value)


class Rating(models.Model):
    """Рейтинг"""

    class Meta:
        db_table = 'Rating'
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    ip = models.CharField('Ip адрес', max_length=15)
    rating_star = models.ForeignKey(RatingStar, verbose_name='Звезда', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Книги', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rating_star} - {self.book}'


class Reviews(models.Model):
    """Отзывы"""

    class Meta:
        db_table = 'Reviews'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    email = models.EmailField()
    title = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщения', max_length=3000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.book}'

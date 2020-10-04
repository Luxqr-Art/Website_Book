from django import forms
from django.contrib import admin

from django.utils.safestring import mark_safe
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BookAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Book
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Квтегории"""
    list_display = ['id', 'title', 'url']
    list_display_links = ['title', ]


# для просмотра отзывов в админке прям прязанных к книгам
class RiviewInline(admin.TabularInline):
    """Отзывы на странице фимльмов"""
    model = Reviews
    extra = 1  # количетво пустых полей для отзывов
    readonly_fields = ['title', 'email']  # только для чтения


class BookShotsInline(admin.TabularInline):
    model = BookShots
    extra = 1
    readonly_fields = ('det_image',)  # внунтри авторов отображаеться картинка

    def det_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="110" height="110"')  # выводим изоброжение в админку

    det_image.short_description = 'Изображение'  # даем название полю в админке


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Книги"""
    list_display = ['title', 'category', 'url', 'draft']
    list_filter = ['category', 'year']
    search_fields = ['title', 'category__title']
    inlines = [BookShotsInline, RiviewInline]  # подключаем класс отзывов выше с привязкой 'RiviewInline', 'BookShotsInline кадры из фильма
    save_on_top = True  # кнопки и сверху и снизу
    save_as = True  # добаватся еще одна кнопка  чтоб сохронялся контент а не переписывать
    actions = ['publish', 'unpublish']
    list_editable = ['draft', ]  # бля булевых значений чтоб устанавливать галочки не входя глубже
    form = BookAdminForm # выводим редактор
    # fields = (('author', 'genre', 'publishing_house'),) # чтоб отображались в один ряд
    # есть еще один более удобный способ он чуть ниже
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline', 'url'),)
        }),
        (None, {
            'fields': (('description', 'draft'),)
        }),
        (None, {
            'fields': (('year', 'country', 'edition', 'category'),)
        }),
        # прячем поля его можно развернуть
        ('Свойства книги', {
            'classes': ('collapse',),
            'fields': (('publishing_house', 'author', 'genre'),)
        }),

        ('Картинка', {
            'fields': (('poster', 'det_image'),)
        }),
    )
    readonly_fields = ('det_image',)  # внунтри авторов отображаеться картинка

    def det_image(self, odj):
        return mark_safe(f'<img src={odj.poster.url} width="80" height="110"')  # выводим изоброжение в админку

    det_image.short_description = 'Изображение'  # даем название полю в админке


# Пишим свои экшенны для админки

    def unpublish(self, request, queryset):
        """Сннять с пудликации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
            self.message_user(request, f'{message_bit}')


    def publish(self, request, queryset):
        """Опудликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
            self.message_user(request, f'{message_bit}')


    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permission = ('change')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ['title', 'parent', 'book', 'id']
    readonly_fields = ['title', 'email']


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    """Издательсво"""
    list_display = ['name', 'url']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ['title', 'url']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Авторы"""
    list_display = ['name', 'age', 'det_image']
    readonly_fields = ('det_image',)  # внунтри авторов отображаеться картинка

    def det_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="50" height="60"')  # выводим изоброжение в админку

    det_image.short_description = 'Изображение'  # даем название полю в админке


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинги"""
    list_display = ['ip', 'rating_star']


@admin.register(BookShots)
class BookShotsAdmin(admin.ModelAdmin):
    """Фото книги"""
    list_display = ['title', 'book', 'det_image']
    readonly_fields = ('det_image',)


    def det_image(self, odj):
        return mark_safe(f'<img src={odj.image.url} width="60" height="50"')


    det_image.short_description = 'Изображение'

admin.site.register(RatingStar)


admin.site.site_title = 'Django Book'   # изменяем название в админке что отображаеться с вверху
admin.site.site_header = "Django Book"

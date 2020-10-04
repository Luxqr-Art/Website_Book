from django import template
from book.models import Category, Book



register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('book/tags/last_book.html')
def det_last_books(count=5):
    books = Book.objects.order_by('id')[:count]
    return {'last_books': books}
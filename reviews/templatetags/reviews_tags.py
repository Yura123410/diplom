from django import template

register = template.Library()


@register.filter(name='stars')
def stars(rating):
    """Преобразует числовой рейтинг в звезды"""
    if not rating or rating == 0:
        return '<span class="text-muted">Нет оценок</span>'

    filled = '<span class="star-filled">★</span>'
    empty = '<span class="star-empty">☆</span>'
    half = '<span class="star-half">½</span>'

    result = ''
    for i in range(1, 6):
        if i <= rating:
            result += filled
        elif i - 0.5 <= rating:
            result += half
        else:
            result += empty

    return result
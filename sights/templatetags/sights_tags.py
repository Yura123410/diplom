from django import template

register = template.Library()


@register.filter()
def sights_media(val):
    if val:
        return val.url
    return '/static/images/no_image.jpg'

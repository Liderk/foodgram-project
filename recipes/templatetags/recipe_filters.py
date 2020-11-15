from django import template
from django.contrib.auth import get_user_model
from recipes.models import FavoriteRecipe, ShoppingTransfer

User = get_user_model()

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def get_tag_filter(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.name in request.GET.getlist('filters'):
        tags = new_request.getlist('filters')
        tags.remove(tag.name)
        new_request.setlist('filters', tags)
    else:
        new_request.appendlist('filters', tag.name)

    return new_request.urlencode()


@register.filter
def get_user_name(value):
    user = User.objects.get(username=value)
    if user.first_name or user.last_name:
        return f'{user.first_name} {user.last_name}'
    return user.username


@register.filter
def is_favorite(recipe, user):
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_shop(recipe, user):
    return ShoppingTransfer.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def shoproster_count(user):
    return ShoppingTransfer.objects.filter(user=user).distinct().count()

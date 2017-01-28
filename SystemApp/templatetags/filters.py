# Django imports
from django import template

register = template.Library()


@register.filter
def item_at(lst, i):
    return lst[i]

# Django imports
from django import template

register = template.Library()


@register.filter
def item_at(lst, i):
    return lst[i]


@register.filter
def pop_item(the_set):
    item = the_set.pop()
    the_set.add(-1)
    return item


@register.filter
def image_name(name):
    return 'images/'+name+'.png'

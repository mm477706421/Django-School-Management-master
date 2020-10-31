from django import template

register = template.Library()


@register.filter(name='num_suffix')
def num_suffix(number):
    if number == 1:
        return '第1名'
    if number == 2:
        return '第2名'
    if number == 3:
        return '第3名'
    if 3 < number <= 12:
        return '第%s' % number

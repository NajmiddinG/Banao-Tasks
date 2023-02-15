from django import template

register = template.Library()

@register.filter(name='trunc')
def trunc(string):
    if len(string)>15:
        return string[:15]+'...'
    return string
from django import template

register = template.Library()

@register.filter
def get_key(value, arg):
    """
    Uset to get value of dictionary. Key is in arg.
    """
    return value[arg]

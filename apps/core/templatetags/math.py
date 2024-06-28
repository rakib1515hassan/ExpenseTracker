from django import template

register = template.Library()


"""
    To Use it in HTML {% load math %} and 
    {{ value1|add:value2 }}
    {{ value1|subtract:value2 }}
    {{ value1|multiply:value2 }}
    {{ value1|divide:value2 }}
    {{ value1|percentage:value2 }}
"""

@register.filter
def add(value, arg):
    try:
        return "{:.2f}".format(float(value) + float(arg))
    except (TypeError, ValueError):
        return ''



@register.filter
def subtract(value, arg):
    try:
        return "{:.2f}".format(float(value) - float(arg))
    except (TypeError, ValueError):
        return ''



@register.filter
def multiply(value, arg):
    try:
        return "{:.2f}".format(float(value) * float(arg))
    except (TypeError, ValueError):
        return ''



@register.filter
def divide(value, arg):
    try:
        return "{:.2f}".format(float(value) / float(arg))
    except (TypeError, ValueError, ZeroDivisionError):
        return ''



@register.filter
def percentage(value, arg):
    try:
        result = (float(value) / 100) * float(arg)
        if result == float('inf') or result == float('-inf'):
            return ''
        return "{:.2f}".format(result)
    except (TypeError, ValueError, ZeroDivisionError):
        return ''
    

@register.filter
def format_number(value):
    try:
        value = float(value)
        return '{:,.2f}'.format(value)
    except (TypeError, ValueError):
        return ''
    

@register.filter(name='format_key')
def format_key(value):
    return value.replace("_", " ").capitalize()

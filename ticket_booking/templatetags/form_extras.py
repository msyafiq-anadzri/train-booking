# your_app/templatetags/form_extras.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a class to a form field."""
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='attr')
def attr(field, attributes):
    """Set an attribute to a form field."""
    key, value = attributes.split(":")
    return field.as_widget(attrs={key: value})

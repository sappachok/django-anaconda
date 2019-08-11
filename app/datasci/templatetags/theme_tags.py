from django import template

register = template.Library()

@register.inclusion_tag('theme/_header.html')
def header():
    return {}

@register.inclusion_tag('theme/_footer.html')
def footer():
    return {}

@register.inclusion_tag('theme/_breadcrumb.html')
def breadcrumb():
    return {}



@register.simple_tag
def template_dir():
    return "http://localhost:8000/static/templates/admin-lte"
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))

@register.filter
def nlbr(html):
    tmp_html = html.replace("\n", "<br>")
    return tmp_html
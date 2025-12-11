from django import template
from apps.kpi_management.translations import get_translation

register = template.Library()


@register.filter(name='trans')
def translate_filter(text, language=None):
    """
    Template filter untuk translation
    Usage: {{ "Dashboard"|trans }} atau {{ "Dashboard"|trans:language }}
    """
    if language is None:
        # Get from context if available
        language = 'id'
    return get_translation(text, language)


@register.simple_tag(name='translate', takes_context=True)
def translate_tag(context, key, language=None):
    """
    Template tag untuk translation
    Usage: {% translate "Dashboard" %} atau {% translate "Dashboard" language %}
    """
    if language is None:
        # Get from context if available
        language = context.get('language', 'id')
    return get_translation(key, language)


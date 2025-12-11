from django.utils.safestring import mark_safe
from django import template
from web_project.template_helpers.theme import TemplateHelper

register = template.Library()


# Register tags as an adapter for the Theme class usage in the HTML template


@register.simple_tag
def get_theme_variables(scope):
    return mark_safe(TemplateHelper.get_theme_variables(scope))


@register.filter
def format_k(value):
    """
    Format angka menjadi format K (contoh: 500000 menjadi 500K)
    """
    try:
        num = float(value)
        if num >= 1000:
            # Konversi ke K (ribuan)
            k_value = num / 1000
            # Jika tidak ada desimal, tampilkan tanpa desimal
            if k_value == int(k_value):
                return f"{int(k_value)}K"
            else:
                # Tampilkan dengan 1 desimal jika perlu
                formatted = f"{k_value:.1f}"
                # Hapus trailing zero dan titik jika tidak perlu
                if formatted.endswith('.0'):
                    return f"{int(k_value)}K"
                return formatted.rstrip('0').rstrip('.') + 'K'
        else:
            # Jika kurang dari 1000, tampilkan angka biasa tanpa desimal jika tidak perlu
            if num == int(num):
                return str(int(num))
            else:
                formatted = f"{num:.1f}"
                # Hapus trailing zero dan titik jika tidak perlu
                if formatted.endswith('.0'):
                    return str(int(num))
                return formatted.rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return value

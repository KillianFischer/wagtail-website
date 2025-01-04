from django import template
from django.core.cache import cache
from home.models import FooterText

register = template.Library()

@register.inclusion_tag('includes/footer_text.html')
def get_footer_text():
    # Try to get footer text from cache first
    footer_text = cache.get('footer_text')
    
    if footer_text is None:
        # If not in cache, get from database
        footer_text = FooterText.objects.filter(live=True).first()
        # Cache the result for 1 hour (3600 seconds)
        if footer_text:
            cache.set('footer_text', footer_text, 3600)

    return {
        'footer_text': footer_text
    }
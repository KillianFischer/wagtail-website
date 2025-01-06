from django import template
from home.models import SocialMediaSettings, FooterSettings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page

@register.inclusion_tag('includes/footer.html', takes_context=True)
def get_footer(context):
    return {
        'footer_settings': FooterSettings.for_site(context['request'].site),
        'social_settings': SocialMediaSettings.for_site(context['request'].site),
        'request': context['request'],
    }
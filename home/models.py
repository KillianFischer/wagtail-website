from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

class HomePage(Page):
    body = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('featured_image'),
    ]

    def get_recent_articles(self):
        articles = Page.objects.live().descendant_of(self).specific()
        articles = articles.order_by('-first_published_at')[:5]
        return articles

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    mastodon_url = models.URLField(blank=True)

    panels = [
        FieldPanel('linkedin_url'),
        FieldPanel('github_url'),
        FieldPanel('mastodon_url'),
    ]

    class Meta:
        verbose_name = 'Social Media Settings'

@register_setting
class FooterSettings(BaseSiteSetting):
    body = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link']
    )

    panels = [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Footer Settings'
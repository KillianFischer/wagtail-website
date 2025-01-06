from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

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

    subpage_types = ['home.NewsPage']

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

class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class NewsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_news_articles(self):
        return ArticlePage.objects.live().descendant_of(self).order_by('-date')

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ArticlePage']

class ArticlePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('tags'),
        FieldPanel('featured_image'),
    ]

    parent_page_types = ['home.NewsPage']
    subpage_types = []
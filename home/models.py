from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from itertools import chain
from operator import attrgetter
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

# Base Article Page for inheritance
class ArticlePageBase(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
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
        FieldPanel('featured_image'),
    ]

    class Meta:
        abstract = True

# Base Index Page for inheritance
class IndexPageBase(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    class Meta:
        abstract = True

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

    # Allow creation of index pages under home
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['home.NewsIndexPage', 'home.ReviewsIndexPage', 'home.TutorialsIndexPage']

    def get_recent_articles(self):
        # Get recent articles from all sections
        news = NewsArticlePage.objects.live().public()
        reviews = ReviewArticlePage.objects.live().public()
        tutorials = TutorialArticlePage.objects.live().public()
        
        # Combine all articles
        all_articles = list(chain(news, reviews, tutorials))
        # Sort by first_published_at
        sorted_articles = sorted(all_articles, key=attrgetter('first_published_at'), reverse=True)
        # Return first 10
        return sorted_articles[:10]

    def get_recent_news(self):
        return NewsArticlePage.objects.live().public().order_by('-first_published_at')[:3]

    def get_recent_reviews(self):
        return ReviewArticlePage.objects.live().public().order_by('-first_published_at')[:3]

    def get_recent_tutorials(self):
        return TutorialArticlePage.objects.live().public().order_by('-first_published_at')[:3]

# News section
class NewsIndexPage(IndexPageBase):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.NewsArticlePage']

    def get_articles(self):
        return NewsArticlePage.objects.live().descendant_of(self).order_by('-date')

class NewsArticlePage(ArticlePageBase):
    parent_page_types = ['home.NewsIndexPage']
    subpage_types = []

# Reviews section
class ReviewsIndexPage(IndexPageBase):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ReviewArticlePage']

    def get_articles(self):
        return ReviewArticlePage.objects.live().descendant_of(self).order_by('-date')

class ReviewArticlePage(ArticlePageBase):
    parent_page_types = ['home.ReviewsIndexPage']
    subpage_types = []

# Tutorials section
class TutorialsIndexPage(IndexPageBase):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.TutorialArticlePage']

    def get_articles(self):
        return TutorialArticlePage.objects.live().descendant_of(self).order_by('-date')

class TutorialArticlePage(ArticlePageBase):
    parent_page_types = ['home.TutorialsIndexPage']
    subpage_types = []

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    panels = [
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('instagram'),
        FieldPanel('youtube'),
    ]

@register_setting
class FooterSettings(BaseSiteSetting):
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('body'),
    ]

class CustomS3Storage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'original_images'
    file_overwrite = False
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    url_protocol = 'https:'
    endpoint_url = settings.AWS_S3_ENDPOINT_URL

class RenditionS3Storage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'images'
    file_overwrite = False
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    url_protocol = 'https:'
    endpoint_url = settings.AWS_S3_ENDPOINT_URL

class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields
    
    storage = CustomS3Storage()

    def get_upload_to(self, filename):
        # Just return the filename since the storage class handles the path
        return filename

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    storage = RenditionS3Storage()

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
from django.shortcuts import render
from wagtail.images import get_image_model
from django.conf import settings

def test_images(request):
    Image = get_image_model()
    images = Image.objects.all()
    return render(request, 'home/test_image.html', {
        'images': images,
        'settings': settings
    }) 
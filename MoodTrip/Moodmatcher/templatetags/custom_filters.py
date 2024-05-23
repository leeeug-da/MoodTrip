# custom_filters.py

from django import template
from django.conf import settings
import os
import random
from urllib.parse import unquote

register = template.Library()

@register.filter(name='file_exists')
def file_exists(value):
    file_path = os.path.join(settings.BASE_DIR, value)
    return os.path.isfile(file_path)

@register.filter(name='get_random_image')
def get_random_image(value):
    image_dir = os.path.join(settings.BASE_DIR, value)
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
    
    if image_files:
        return os.path.join(value, random.choice(image_files))
    else:
        return None

@register.filter(name='urldecode')
def urldecode(value):
    return unquote(value)
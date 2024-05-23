# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.staticfiles import finders



### tour_db

class TourCategory(models.Model):
    tour_cat_id = models.AutoField(primary_key=True)
    tour_cat_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_category'


class TourEtc(models.Model):
    tour = models.ForeignKey('TourMain', models.DO_NOTHING, blank=True, null=True, related_name='tour_etc_set_for_tour')
    tour_cat = models.ForeignKey('TourMain', models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_etc_set_for_tour_cat')
    stroller = models.TextField(blank=True, null=True)
    pet = models.TextField(blank=True, null=True)
    parking = models.TextField(blank=True, null=True)
    parking_fare = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_etc'


class TourImgPath(models.Model):
    tour = models.ForeignKey('TourMain', models.DO_NOTHING, blank=True, null=True, related_name='tour_img_path_set_for_tour')
    tour_cat = models.ForeignKey('TourMain', models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_img_path_set_for_tour_cat')
    img_path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_img_path'


class TourInfo(models.Model):
    tour = models.ForeignKey('TourMain', models.DO_NOTHING, blank=True, null=True, related_name='tour_info_set_for_tour')
    tour_cat = models.ForeignKey('TourMain', models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_info_set_for_tour_cat')
    intro = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    guide = models.TextField(blank=True, null=True)
    price_1 = models.TextField(blank=True, null=True)
    price_2 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_info'


class TourKeyRat(models.Model):
    tour = models.ForeignKey('TourMain', models.DO_NOTHING, blank=True, null=True, related_name='tour_key_rat_set_for_tour')
    tour_cat = models.ForeignKey('TourMain', models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_key_rat_set_for_tour_cat')
    key_1 = models.TextField(blank=True, null=True)
    key_2 = models.TextField(blank=True, null=True)
    key_3 = models.TextField(blank=True, null=True)
    ratings = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_key_rat'


class TourKeywords(models.Model):
    tour = models.ForeignKey('TourMain', models.DO_NOTHING, blank=True, null=True, related_name='tour_keywords_set_for_tour')
    tour_cat = models.ForeignKey('TourMain', models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_keywords_set_for_tour_cat')
    key_1 = models.TextField(blank=True, null=True)
    key_2 = models.TextField(blank=True, null=True)
    key_3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_keywords'


class TourMain(models.Model):
    tour_id = models.AutoField(primary_key=True)
    tour_cat = models.ForeignKey(TourCategory, models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_main'
        constraints = [
            models.UniqueConstraint(fields=['tour_cat'], name='unique_tour_cat')
        ]


class TourPeriod(models.Model):
    tour = models.ForeignKey(TourMain, models.DO_NOTHING, blank=True, null=True, related_name='tour_period_set_for_tour')
    tour_cat = models.ForeignKey(TourMain, models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_period_set_for_tour_cat')
    open_hour_1 = models.TextField(blank=True, null=True)
    open_hour_2 = models.TextField(blank=True, null=True)
    open_hour_3 = models.TextField(blank=True, null=True)
    close_day = models.TextField(blank=True, null=True)
    open_period_1 = models.TextField(blank=True, null=True)
    open_period_2 = models.TextField(blank=True, null=True)
    fest_open = models.TextField(blank=True, null=True)
    fest_close = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_period'


class TourRatings(models.Model):
    tour = models.ForeignKey(TourMain, models.DO_NOTHING, blank=True, null=True, related_name='tour_ratings_set_for_tour')
    tour_cat = models.ForeignKey(TourMain, models.DO_NOTHING, to_field='tour_cat_id', blank=True, null=True, related_name='tour_ratings_set_for_tour_cat')
    ratings = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_ratings'



###### default


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, default='community')  # 또는 'customer-service'로 설정
    likes = models.ManyToManyField(User, related_name='liked_posts')  # 여기서 related_name을 업데이트하세요
    new_likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)

    def __str__(self):
        return f"Image {self.title}"

    
    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return f"Image {self.pk}"


def default_profile_picture():
    default_image_path = finders.find('images/default_profile.png')

    if default_image_path:
        default_image_path = default_image_path.replace("\\", "/")  # Windows 경로에서 슬래시로 변경
    else:
        default_image_path = '/static/images/profile.png'

    return default_image_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default=default_profile_picture)

    def __str__(self):
        return self.user.username


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'




from django.db import models

class TouristSpot(models.Model):
    # 필요한 필드들을 추가
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_spot_images/')

    def __str__(self):
        return self.name
    
############
class SelectedImage(models.Model):
    image = models.ImageField(upload_to='selected_images/')

    def get_image_url(self):
        return self.image.url
    
from django import forms
    
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
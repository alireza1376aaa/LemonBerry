from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from User_Setting.models import autentication
from Web_inher.models import Category_web, Tag, Gallery, Gender
from django.utils.text import slugify
from polls.views import remove_spaces
from django.core.validators import MaxValueValidator


# Create your models here.


class more_discription(models.Model):
    title_seasionone = models.CharField(max_length=200, null=True, blank=True)
    discription_seasionone = models.TextField(null=True, blank=True)
    title_seasiontwo = models.CharField(max_length=200, null=True, blank=True)
    discription_seasiontwo = models.TextField(null=True, blank=True)
    title_seasiontree = models.CharField(max_length=200, null=True, blank=True)
    discription_seasiontree = models.TextField(null=True, blank=True)


class web_log(models.Model):
    title = models.CharField(max_length=100)
    main_title = models.CharField(max_length=100, null=True, blank=True)
    shortdescription = models.CharField(max_length=500)
    discription = models.TextField()
    extra_discription = models.OneToOneField(to=more_discription, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    main_photo = models.ImageField(upload_to='upload/weblog_main/%Y/%m/%d', null=True, blank=True)
    auter = models.ForeignKey(to=autentication, on_delete=models.CASCADE)
    category_web_model = models.ManyToManyField(Category_web)
    gender = models.ForeignKey(to=Gender, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(to=Tag, related_name='weblog_tag')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True)
    satisfaction_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = f'{remove_spaces(slugify(self.title))}_{slugify(get_random_string(4))}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('detail_weblog', kwargs={'category': self.title, 'slug': self.slug})

    def edit_blog(self):
        return reverse('edit_weblog', kwargs={'pk': self.id})

    def get_absolut_url_admin(self):
        return reverse('blog_details_admin', args=[self.slug])


class Web_log_Comment(models.Model):
    article = models.ForeignKey(web_log, on_delete=models.CASCADE)
    parent = models.ForeignKey('Web_log_Comment', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(autentication, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return str(self.id)


class Rate_of_Blog(models.Model):
    weblod = models.ForeignKey(web_log, on_delete=models.CASCADE, related_name='rate_set')
    user = models.ForeignKey(autentication, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return str(self.weblod.id)

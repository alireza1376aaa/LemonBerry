from django.db import models

from polls.views import remove_spaces


# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=20)
    image1 = models.ImageField(upload_to='upload/weblog/%Y/%m/%d', null=True, blank=True)
    image2 = models.ImageField(upload_to='upload/weblog/%Y/%m/%d', null=True, blank=True)
    image3 = models.ImageField(upload_to='upload/weblog/%Y/%m/%d', null=True, blank=True)
    image4 = models.ImageField(upload_to='upload/weblog/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.title


class Category_web(models.Model):
    parent = models.ForeignKey(to='Category_web', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.url_title = remove_spaces(self.title)
        return super().save(*args, **kwargs)


class Gender(models.Model):
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.url_title = remove_spaces(self.title)
        return super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.url_title = self.title.replace(" ", "_")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Region(models.Model):
    city = models.CharField(max_length=200)
    village = models.ForeignKey('Region', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

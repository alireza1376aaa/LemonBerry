from django.db import models
from User_Setting.models import autentication


# Create your models here.

class About_us(models.Model):
    Welcome_message_text = models.CharField(max_length=200)
    Title_description = models.CharField(max_length=200)
    Main_description = models.TextField()
    Image_for_About = models.ImageField(upload_to='upload/Site_Setting/About', null=True, blank=True)
    part1_description = models.CharField(max_length=200, null=True, blank=True)
    part1_body = models.TextField(null=True, blank=True)
    part2_description = models.CharField(max_length=200, null=True, blank=True)
    part2_body = models.TextField(null=True, blank=True)
    part3_description = models.CharField(max_length=200, null=True, blank=True)
    part3_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.Title_description


class Contact_Us(models.Model):
    User = models.ForeignKey(autentication, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=100)
    Text_massage = models.TextField()
    response = models.TextField(null=True, blank=True)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return self.Subject


class Site_Setting(models.Model):
    Address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    Email = models.EmailField()
    Website = models.CharField(max_length=200)
    Address_map = models.URLField(max_length=500)
    Logo_web = models.ImageField(upload_to='upload/Site_Setting/logo')
    Main_photo = models.ImageField(upload_to='upload/Site_Setting/Main_photo')
    text_wellcome_firstpage = models.CharField(max_length=200)
    about_website = models.CharField(max_length=400)
    link_instagram = models.URLField()
    link_telegram = models.URLField()
    link_x = models.URLField()
    text_for_rule = models.CharField(max_length=400)


class photo_page(models.Model):
    about_us_img = models.ImageField(upload_to='upload/Site_Setting/Photo_page')
    list_weblog_img = models.ImageField(upload_to='upload/Site_Setting/Photo_page')
    text_for_listweblog = models.CharField(max_length=500, null=True, blank=True)
    contact_us_img = models.ImageField(upload_to='upload/Site_Setting/Photo_page')
    make_blog_img = models.ImageField(upload_to='upload/Site_Setting/Photo_page')


class Team_about(models.Model):
    fullname = models.CharField(max_length=100)
    img = models.ImageField(upload_to='upload/Site_Setting/Team_about')
    job = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.fullname

class UserVisit(models.Model):
    visited_ip = models.CharField(max_length=200,unique=True)
    date = models.DateField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.visited_ip
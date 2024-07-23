from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.

class autentication(AbstractUser):
    image_pro = models.ImageField(upload_to='upload/profile/%Y/%m/%d', null=True, blank=True,
                                  default='upload/profile/defult_pro.png')
    # username
    # firstname
    # latname
    main_location = models.CharField(max_length=100, null=True, blank=True, )
    location = models.CharField(max_length=100, null=True, blank=True, )
    # email
    phone = models.CharField(max_length=11, null=True, blank=True, )
    date_birth = models.DateField(null=True, blank=True, )
    about_user = models.TextField(max_length=500, null=True, blank=True, )
    verify_code = models.CharField(max_length=100, default='')
    is_verify = models.BooleanField(default=False)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolut_url(self):
        return reverse('details_user_p', kwargs={'pk': self.id})

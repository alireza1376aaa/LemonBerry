from django.urls import path
from WebLogSetting.views import Home,AboutUs,Contact_us,Check_email,Send_Contact
urlpatterns = [
    path('',Home.as_view(),name='Home_page'),
    path('about', AboutUs.as_view(), name='About_us_page'),
    path('contact', Contact_us.as_view(), name='Contact_us_page'),
    path('contact/chekemail', Check_email.as_view()),
    path('contact/chekemail/send_contact', Send_Contact.as_view()),

]
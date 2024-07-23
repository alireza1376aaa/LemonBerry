from django.shortcuts import render
from django.views.generic import TemplateView, View
from User_Setting.models import autentication
from django.http import HttpResponse, JsonResponse
from WebLogSetting.models import Contact_Us, About_us, photo_page, Team_about, Site_Setting
import itertools
from .models import UserVisit


# Create your views here.


class Home(View):
    def get(self, request):
        try:
            visit = self.request.META['USERDOMAIN']
            get_visit = UserVisit.objects.filter(visited_ip=visit)
            if get_visit.exists():
                get_visit = get_visit.first()
                get_visit.count += 1
                get_visit.save()
            else:
                get_visit = UserVisit.objects.create(visited_ip=visit)
        except:
            pass
        context = {'site_setting': Site_Setting.objects.first()}
        return render(request, 'Home_page/Home_page.html', context)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


class AboutUs(TemplateView):
    template_name = 'About_us/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUs, self).get_context_data()
        context['About_us'] = About_us.objects.first()
        context['photo_page'] = photo_page.objects.first()
        myteam = my_grouper(3, Team_about.objects.all())
        context['colleague'] = myteam

        return context


class Contact_us(View):
    def get(self, request):
        context = {'photo_page': photo_page.objects.first(), 'site_setting': Site_Setting.objects.first()}

        return render(request, 'Contact_us/Contact.html', context)


class Send_Contact(View):
    def get(self, request):
        Email_address = request.GET.get('email_ad')
        Subject = request.GET.get('subject')
        Massage = request.GET.get('massage')

        clientuser = autentication.objects.filter(email__iexact=Email_address)
        if clientuser.exists():
            new_comment = Contact_Us(User=clientuser.first(), Subject=Subject, Text_massage=Massage)
            new_comment.save()
            return HttpResponse('Send Your Massage Success')
        else:
            return HttpResponse('Send Your Massage Error')


class Check_email(View):
    def get(self, request):
        Email_address = request.GET.get('email_ad')
        clientuser = autentication.objects.filter(email__iexact=Email_address)
        if clientuser.exists():
            return HttpResponse('')
        else:
            return HttpResponse('This Email Is Not Exists')

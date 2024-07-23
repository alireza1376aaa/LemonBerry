from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, Http404
from django.utils.crypto import get_random_string
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from WebLog.models import web_log
from WebLogSetting.models import Contact_Us
from .form import Register_form, log_in_form, password_form
from .models import autentication
from .send_email import send_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


class Register_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Edit_Profile')
        myform = Register_form()
        context = {'register_form': myform}
        return render(request, 'Register/register.html', context)

    def post(self, request):
        myform = Register_form(request.POST)
        if myform.is_valid():
            username = myform.cleaned_data['username']
            email = myform.cleaned_data['email']
            Password = myform.cleaned_data['Password']
            User = autentication.objects.filter(Q(username__iexact=username) | Q(email__iexact=email))
            if User.exists():
                for myerror in User.all():
                    if myerror.username == username:
                        myform.add_error('username', 'username is exsit')
                    elif myerror.email == email:
                        myform.add_error('email', ' email is exsit')

            else:
                NewUser = autentication.objects.create(username=username, email=email,
                                                       verify_code=get_random_string(99), is_verify=False)
                NewUser.set_password(Password)

                NewUser.save()

                send_email('verify Account', NewUser.email, {'user': NewUser}, 'email/send_email.html')
                return redirect('log_in')
        context = {'register_form': myform}
        return render(request, 'Register/register.html', context)


def Verify_account(request, verifycode):
    mycode = verifycode
    user = autentication.objects.filter(verify_code__iexact=mycode).first()
    if user is not None:
        if user.is_verify == False:
            user.is_verify = True
            user.verify_code = get_random_string(99)
            user.save()
            messages.success(request, "veryfi account you successfully")
            return redirect("/")
        else:
            messages.warning(request, 'you are veryfy past')
            return redirect("/")
    else:
        return Http404


class Log_in(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Edit_Profile')
        myform = log_in_form()
        contex = {'log_in': myform}
        return render(request, 'Log_in/log_in_page.html', contex)

    def post(self, request):
        myform = log_in_form(request.POST)
        if myform.is_valid():
            username = myform.cleaned_data['usernameoremail']
            Password = myform.cleaned_data['password']
            User = autentication.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if User is not None:
                if not User.is_verify:
                    myform.add_error('usernameoremail', 'user is not active')
                else:
                    if User.check_password(Password):
                        login(request, User)
                        return redirect('Edit_Profile')
                    else:
                        myform.add_error('password', 'password is not correct')

            else:
                myform.add_error('usernameoremail', 'user is not valid')

        contex = {'log_in': myform}
        return render(request, 'Log_in/log_in_page.html', contex)


def forgot_pass_first(request):
    if request.POST:
        email = request.POST['email']
        user = autentication.objects.filter(email__iexact=email).first()
        if user is not None:
            send_email('password Account', user.email, {'user': user}, 'email/send_email_password.html')
            return redirect('log_in')

    return render(request, 'Log_in/forgetPassword_email.html', {})


def forgot_pass(request, verifycode):
    verifycodepass = verifycode
    user = autentication.objects.filter(verify_code__iexact=verifycodepass).first()

    if user is not None:
        myform = password_form(request.POST)
        if myform.is_valid():
            new_password = myform.cleaned_data['Password']
            user.set_password(new_password)
            user.verify_code = get_random_string(99)
            user.save()
            return redirect('log_in')
        else:
            myform.add_error("Password", 'complit your fild')
    else:
        raise Http404()
    contex = {'forget_pass': myform}
    return render(request, 'Log_in/forgotPassword.html', contex)


def edit_profile(request):
    my_user = None
    if request.user.is_authenticated:
        my_user = autentication.objects.get(id=request.user.id)

        if request.method == 'POST':
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            mainlocation = request.POST['mainlocation']
            location = request.POST['location']
            email = request.POST['email']
            phonenamber = request.POST['phonenamber']
            birthday = request.POST['birthday']
            yourself_about = request.POST['yourself_about']

            x = request.FILES
            if len(x) != 0:

                img_pro = request.FILES['img_pro']
                img_pro.name = f'{username}+{get_random_string(9)}.png'
                if img_pro.size > 5000000:
                    messages.error(request, "more than 5MB")
                    img_pro = my_user.image_pro

            truth_change = True

            User = autentication.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=email) | Q(phone__iexact=phonenamber))
            if User.exists():
                for myerror in User.all():
                    if myerror.username == username and myerror.username != my_user.username:
                        truth_change = False
                        messages.error(request, 'username is exists')
                    elif myerror.email == email and myerror.email != my_user.email:
                        truth_change = False
                        messages.error(request, 'email is exists')
                    elif myerror.phone == phonenamber and myerror.phone != my_user.phone:
                        truth_change = False
                        messages.error(request, 'phone is exists')

            if truth_change == True:
                my_user.username = username
                my_user.first_name = firstname
                my_user.last_name = lastname
                my_user.main_location = mainlocation
                my_user.location = location
                my_user.email = email
                my_user.phone = phonenamber
                my_user.about_user = yourself_about
                if len(birthday) != 0:
                    my_user.date_birth = birthday
                if len(x) != 0:
                    my_user.image_pro = img_pro
                my_user.save()


    else:
        return redirect('log_in')

    context = {'user': my_user}
    return render(request, 'Register/edit_profile.html', context)


class Log_out(View):
    def get(self, request):
        logout(request)
        return redirect('log_in')


@method_decorator(login_required(login_url='log_in'), name='dispatch')
class wait(TemplateView):
    template_name = 'wait_panel/wait.html'

    def get_context_data(self, **kwargs):
        context = super(wait, self).get_context_data()
        request = self.request
        context['blog'] = web_log.objects.filter(auter_id=request.user.id)
        return context


@method_decorator(login_required(login_url='log_in'), name='dispatch')
class ticket(TemplateView):
    template_name = 'wait_panel/ticket.html'

    def get_context_data(self, **kwargs):
        context = super(ticket, self).get_context_data()
        request = self.request
        context['massagebox'] = Contact_Us.objects.filter(User_id=request.user.id)
        return context

from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib.auth import login
from django.views.generic import TemplateView, View, ListView, DetailView
from WebLog.models import web_log
from Web_inher.models import Category_web, Gender
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from User_Setting.models import autentication
from WebLogSetting.models import Site_Setting, photo_page, About_us, Contact_Us, Team_about
from WebLogSetting.models import UserVisit


# Create your views here.
class Log_in(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('adminpanel')
            else:
                raise Http404
        else:
            return render(request, 'Log_in_admin/Log_in.html', {})

    def post(self, request):
        username = request.POST.get('userName')
        password = request.POST.get('password')
        context = {'Error': ''}
        if len(username) > 3 and len(password) > 3:
            try:
                User = autentication.objects.get(username__iexact=username, is_superuser=True)
            except:
                User = None

            if User is not None:
                if User.check_password(password):
                    login(request, User)
                    return redirect('adminpanel')
                else:
                    context['Error'] = 'password is not correct'

            else:
                context['Error'] = 'user is not valid'
        else:
            context['Error'] = 'Check Your username and password'

        return render(request, 'Log_in_admin/Log_in.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class panel_admin(TemplateView):
    template_name = 'panel_admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(panel_admin, self).get_context_data()
        count_log = web_log.objects.filter(is_active=False).count()
        context['count'] = count_log
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class Weblog_Admin(TemplateView):
    template_name = 'panel_admin/weblog.html'

    def get_context_data(self, **kwargs):
        context = super(Weblog_Admin, self).get_context_data()
        count_log = web_log.objects.filter(is_active=False).count()
        context['count'] = count_log
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class List_Blog_deactive(ListView):
    model = web_log
    template_name = 'weblog_panel/list_deactive_blog.html'
    context_object_name = 'blog'

    def get_queryset(self):
        data = super(List_Blog_deactive, self).get_queryset()
        data = data.filter(is_active=False, is_delete=False).order_by('date')
        return data


@user_passes_test(lambda u: u.is_superuser)
def short_cut_active_delete(request):
    if request.method == 'GET':
        path_url = request.GET.get('path_url')
        id_active = dict(request.GET)
        try:
            actives = id_active['short_active']
        except:
            actives = []
        try:
            all = id_active['blog_id']
        except:
            all = []
        try:
            delete = id_active['short_delete']
        except:
            delete = []
        deactiv = list(set(actives) ^ set(all))
        ondelet = list(set(delete) ^ set(all))

        if len(actives) > 0 or len(deactiv) > 0:
            for active in actives:
                x = web_log.objects.filter(pk=active).first()
                x.is_active = True
                x.save()
            if len(all) > 0:
                for deactive in deactiv:
                    x = web_log.objects.filter(pk=deactive).first()
                    x.is_active = False
                    x.save()
        if len(delete) > 0 or len(ondelet) > 0:
            for deleted in delete:
                x = web_log.objects.filter(pk=deleted).first()
                x.is_delete = True
                x.is_active = False
                x.save()

            if len(all) > 0:
                for ondeleted in ondelet:
                    x = web_log.objects.filter(pk=ondeleted).first()
                    x.is_delete = False
                    x.save()

    return redirect(path_url)


@user_passes_test(lambda u: u.is_superuser)
def Show_blog_details(request, a_blog_d):
    try:
        details_blog = web_log.objects.get(slug__exact=a_blog_d)

    except:
        details_blog = None
    context = {'blog': details_blog}
    return render(request, 'weblog_panel/details_blog.html', context)


@user_passes_test(lambda u: u.is_superuser)
def active_or_deactive(request):
    if request.method == 'GET':
        value_blog = request.GET.get('activate_val')
        id_blog = request.GET.get('activate_id')

        if value_blog == 'True':
            try:
                ac_blog = web_log.objects.get(id=int(id_blog))
                ac_blog.is_active = True
                ac_blog.save()
            except:
                ac_blog = None
        else:
            try:
                ac_blog = web_log.objects.get(id=int(id_blog))
                ac_blog.is_active = False
                ac_blog.save()

            except:
                ac_blog = None

    return redirect('weblog_admin')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class List_Categoryh(ListView):
    model = Category_web
    template_name = 'weblog_panel/add_category.html'
    context_object_name = 'cat'
    ordering = 'title'


@user_passes_test(lambda u: u.is_superuser)
def change_cat(request):
    if request.method == 'GET':
        id_category = request.GET.get('id_category')
        parent_add_cat_detail = request.GET.get('parent_add_cat_detail')
        title = request.GET.get('title')
        active_deactive = request.GET.get('active_deactive')
        try:
            edit_cat = Category_web.objects.get(id=id_category)
        except:
            redirect('list_category_add')
        if len(parent_add_cat_detail) > 0:
            edit_cat.parent_id = int(parent_add_cat_detail)

        if len(title) > 0:
            edit_cat.title = title

        if len(active_deactive) > 0:
            if active_deactive == 'true':
                edit_cat.is_active = True
            else:
                edit_cat.is_active = False

        edit_cat.save()

    return redirect('list_category_add')


@user_passes_test(lambda u: u.is_superuser)
def Add_category(request):
    if request.method == 'GET':
        parent_add_cat = request.GET.get('parent_add_cat')
        Add_Title = request.GET.get('title_cat_add')

        if parent_add_cat is None:
            add_cat = Category_web.objects.create(title=Add_Title, is_active=True)
        else:
            add_cat = Category_web.objects.create(parent_id=int(parent_add_cat), title=Add_Title, is_active=True)

    return redirect('list_category_add')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class List_Genre(ListView):
    model = Gender
    template_name = 'weblog_panel/add_genre.html'
    context_object_name = 'gen'
    ordering = 'title'


@user_passes_test(lambda u: u.is_superuser)
def change_gen(request):
    if request.method == 'GET':
        id_gener = request.GET.get('id_gener')
        title = request.GET.get('title')
        active_deactive = request.GET.get('active_deactive')
        try:
            edit_gen = Gender.objects.get(id=id_gener)
        except:
            redirect('list_genre_add')

        if len(title) > 0:
            edit_gen.title = title

        if len(active_deactive) > 0:
            if active_deactive == 'true':
                edit_gen.is_active = True
            else:
                edit_gen.is_active = False

        edit_gen.save()

    return redirect('list_genre_add')


@user_passes_test(lambda u: u.is_superuser)
def Add_genre(request):
    if request.method == 'GET':
        Add_Title = request.GET.get('title_gen_add')
        add_cat = Gender.objects.create(title=Add_Title, is_active=True)

    return redirect('list_genre_add')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class List_Blog_admin(ListView):
    model = web_log
    template_name = 'weblog_panel/list_blog.html'
    context_object_name = 'blog'
    ordering = '-satisfaction_percentage'


# ///////////////////////////////////////////////////////////////////////////
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class User_panel(TemplateView):
    template_name = 'user_panel/user_panel.html'
    def get_context_data(self, **kwargs):
        context = super(User_panel,self).get_context_data()
        context['count_all'] = autentication.objects.all().count()
        context['count_all_visit'] = UserVisit.objects.all().count()
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class List_user(ListView):
    model = autentication
    template_name = 'user_panel/list_user.html'
    context_object_name = 'user'
    ordering = 'date_joined'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class Detail_user(DetailView):
    model = autentication
    template_name = 'user_panel/detail_user.html'
    context_object_name = 'user'


# ///////////////////////////////////////////////////////////////////////////

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class Setting_panel(TemplateView):
    template_name = 'setting/setting.html'

    def get_context_data(self, **kwargs):
        context = super(Setting_panel, self).get_context_data()
        massage_count: Contact_Us = Contact_Us.objects.filter(visited=False).count()
        context['count'] = massage_count
        return context


@user_passes_test(lambda u: u.is_superuser)
def Get_img_page(request):
    page_img = photo_page.objects.first()
    main_page = Site_Setting.objects.first()

    if request.method == 'POST':
        if main_page is None:
            main_page = Site_Setting.objects.create()
        if page_img is None:
            page_img = photo_page.objects.create()

        main_picture = request.FILES.get('mainpage')
        About_Us_Page = request.FILES.get('About_Us_Page')
        List_Weblog_Page = request.FILES.get('List_Weblog_Page')
        text_massage_list = request.POST.get('text_massage_list')
        Contact_Us_Page = request.FILES.get('Contact_Us_Page')
        Make_Blog_Page = request.FILES.get('Make_Blog_Page')

        if main_picture is not None:
            main_page.Main_photo = main_picture
            main_page.save()

        if About_Us_Page is not None:
            page_img.about_us_img = About_Us_Page
            page_img.save()

        if List_Weblog_Page is not None:
            page_img.list_weblog_img = List_Weblog_Page
            page_img.save()

        if len(text_massage_list) > 0:
            page_img.text_for_listweblog = text_massage_list
            page_img.save()

        if Contact_Us_Page is not None:
            page_img.contact_us_img = Contact_Us_Page
            page_img.save()

        if Make_Blog_Page is not None:
            page_img.make_blog_img = Make_Blog_Page
            page_img.save()

    context = {'page_img': page_img, 'main_page': main_page}
    return render(request, 'setting/image_setting.html', context)


@user_passes_test(lambda u: u.is_superuser)
def Site_setting_page(request):
    main_page = Site_Setting.objects.first()

    if request.method == 'POST':
        if main_page is None:
            main_page = Site_Setting.objects.create()

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        website = request.POST.get('website')
        googleaddress = request.POST.get('googleaddress')
        text_wellcom = request.POST.get('biginertext')
        about_web = request.POST.get('about_web')
        rule = request.POST.get('rule')
        instagram = request.POST.get('instagram')
        telegram = request.POST.get('telegram')
        twitter = request.POST.get('twitter')
        logo_img = request.FILES.get('logo_img')

        if len(email) > 0:
            main_page.Email = email
            main_page.save()
        if len(phone) > 0:
            main_page.Phone = phone
            main_page.save()
        if len(address) > 0:
            main_page.Address = address
            main_page.save()
        if len(website) > 0:
            main_page.Website = website
            main_page.save()
        if len(googleaddress) > 0:
            main_page.Address_map = googleaddress
            main_page.save()
        if len(text_wellcom) > 0:
            main_page.text_wellcome_firstpage = text_wellcom
            main_page.save()
        if len(about_web) > 0:
            main_page.about_website = about_web
            main_page.save()
        if len(rule) > 0:
            main_page.text_for_rule = rule
            main_page.save()
        if len(instagram) > 0:
            main_page.link_instagram = instagram
            main_page.save()
        if len(telegram) > 0:
            main_page.link_telegram = telegram
            main_page.save()
        if len(twitter) > 0:
            main_page.link_x = twitter
            main_page.save()

        if logo_img is not None:
            main_page.Logo_web = logo_img
            main_page.save()

    context = {'main_page': main_page}
    return render(request, 'setting/site_setting.html', context)


@user_passes_test(lambda u: u.is_superuser)
def About_setting_page(request):
    main_page = About_us.objects.first()

    if request.method == 'POST':
        if main_page is None:
            main_page = About_us.objects.create()
        img_about = request.FILES.get('img_about')
        wellcom_about = request.POST.get('wellcom_about')
        title_descr = request.POST.get('title_descr')
        main_descr = request.POST.get('main_descr')
        title1_descr = request.POST.get('title1_descr')
        main1descr = request.POST.get('main1descr')
        title2_descr = request.POST.get('title2_descr')
        main2descr = request.POST.get('main2descr')
        title3_descr = request.POST.get('title3_descr')
        main3descr = request.POST.get('main3descr')

        if len(wellcom_about) > 0:
            main_page.Welcome_message_text = wellcom_about
            main_page.save()
        if len(title_descr) > 0:
            main_page.Title_description = title_descr
            main_page.save()
        if len(main_descr) > 0:
            main_page.Main_description = main_descr
            main_page.save()
        if len(title1_descr) > 0:
            main_page.part1_description = title1_descr
            main_page.save()
        if len(main1descr) > 0:
            main_page.part1_body = main1descr
            main_page.save()
        if len(title2_descr) > 0:
            main_page.part2_description = title2_descr
            main_page.save()
        if len(main2descr) > 0:
            main_page.part2_body = main2descr
            main_page.save()
        if len(title3_descr) > 0:
            main_page.part3_description = title2_descr
            main_page.save()
        if len(main3descr) > 0:
            main_page.part3_body = main2descr
            main_page.save()

        if img_about is not None:
            main_page.Image_for_About = img_about
            main_page.save()

    context = {'main_page': main_page}
    return render(request, 'setting/About_us_setting.html', context)


@user_passes_test(lambda u: u.is_superuser)
def Add_Employee_page(request):
    main_page = Team_about.objects.all()
    if request.method == 'POST':
        name_member = request.POST.get('name_member')
        job_member = request.POST.get('job_member')
        about_member = request.POST.get('about_member')
        Make_profile = request.FILES.get('Make_profile')

        if len(name_member) > 0 and len(job_member) > 0 and len(about_member) > 0 and Make_profile is not None:
            creat_member = Team_about.objects.create(fullname=name_member, job=job_member, about=about_member,
                                                     img=Make_profile)

    context = {'main_page': main_page}
    return render(request, 'setting/Add_employee.html', context)


@user_passes_test(lambda u: u.is_superuser)
def remove_Employee(request, id_em):
    try:
        main_page = Team_about.objects.get(id=id_em).delete()
    except:
        pass
    return redirect("add_employee_page")


@user_passes_test(lambda u: u.is_superuser)
def Contact_admin_page(request):
    main_page = Contact_Us.objects.all()

    if request.method == 'POST':
        id_massage = request.POST.get('id_massage')
        answer = request.POST.get('answer')

        if len(id_massage) > 0 and len(answer) > 0:
            response = main_page.get(id=int(id_massage))
            response.response = answer
            response.visited = True
            response.save()

    context = {'main_page': main_page}
    return render(request, 'setting/list_contact_massage.html', context)


def visited(request):
    visited = UserVisit.objects.all()
    context = {'user': visited}
    return render(request, 'user_panel/list_visit.html', context)

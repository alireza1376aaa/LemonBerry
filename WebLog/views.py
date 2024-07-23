from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, DetailView, View, UpdateView
from .models import web_log, Web_log_Comment, Rate_of_Blog, more_discription
from Web_inher.models import Tag, Gender, Gallery
import itertools
from Web_inher.models import Category_web
from WebLogSetting.models import photo_page
from django.db.models import Sum, Q
from .form import Make_Weblog, Make_Weblog_section2, Make_Weblog_section3, Make_Weblog_section4
from .edit_form import Edit_Form, Edit_form_img, Edit_form_extra
from django.urls import reverse_lazy


# Create your views here.
def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


class List_weblog(ListView):
    model = web_log
    template_name = 'list_view/list_weblog.html'
    paginate_by = 6
    context_object_name = 'web_log'
    ordering = '-date'

    def my_category(self):
        mycategory = Category_web.objects.filter(is_active=True)
        return mycategory

    def my_gender(self):
        mygender = Gender.objects.filter(is_active=True)
        return mygender

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(List_weblog, self).get_context_data()
        grouped_related_products_cat = list(my_grouper(4, self.my_category()))
        grouped_related_products_gen = list(my_grouper(4, self.my_gender()))
        sitesetting = photo_page.objects.first()

        context['category'] = grouped_related_products_cat
        context['Gender'] = grouped_related_products_gen
        context['sitesetting'] = sitesetting

        return context

    def get_queryset(self):
        data = super(List_weblog, self).get_queryset()
        data = data.filter(is_delete=False, is_active=True)
        category = self.request.resolver_match.kwargs['category']
        tag_search = data.filter(tag__url_title=category).all()

        listofcategory = list()
        listofgender = list()

        for categorys in self.my_category():
            listofcategory.append(categorys.url_title)

        for genders in self.my_gender():
            listofgender.append(genders.url_title)

        if category in listofcategory:
            data = data.filter(
                Q(category_web_model__url_title=category) | Q(category_web_model__parent__url_title=category))
            return data
        elif category in listofgender:
            data = data.filter(gender__url_title=category)
            return data
        elif tag_search.exists():
            data = tag_search
        elif category != 'weball':
            raise Http404("Not found")
        return data


class Filter_web(View):
    xs = []

    def get(self, request, *args, **kwargs):
        myfilter = request.GET.get('filter')
        page_number = request.GET.get("page")
        if myfilter != None or page_number != None:
            self.xs.append(myfilter)
            if myfilter is None:
                pass
            else:
                self.xs[0] = myfilter

            newdata = web_log.objects.filter(is_delete=False, is_active=True).order_by(self.xs[0])
            paginator = Paginator(newdata, 6)
            page_obj = paginator.get_page(page_number)
            context = {'web_log': page_obj, "page_obj": page_obj, 'paginator': paginator}
            return render(request, 'list_view/include_list.html', context)

        else:
            return redirect("list_weblog", category='weball')


class Search_web(View):
    xs = []

    def get(self, request, *args, **kwargs):
        mysearch = request.GET.get('search')
        page_number = request.GET.get("page")
        if mysearch != None or page_number != None:
            self.xs.append(mysearch)
            if mysearch is None:
                pass
            else:
                self.xs[0] = mysearch

            newdata = web_log.objects.filter(title__icontains=mysearch, is_delete=False, is_active=True).order_by(
                '-date')

            context = {'web_log': newdata}
            return render(request, 'list_view/include_list.html', context)

        else:
            return redirect("list_weblog", category='weball')


class Detail_weblog(DetailView):
    model = web_log
    template_name = 'detail_view/datail_view.html'
    context_object_name = 'web_log'

    def rate_of_blog(self, web_log_id):
        myobject = Rate_of_Blog.objects.filter(weblod_id=web_log_id).all()
        count = myobject.count()
        sumscore = myobject.aggregate(Sum('score'))
        if count and sumscore is not None:
            rate_blog = {'count': count, 'rate': int((sumscore['score__sum'] / count) * 20)}
            return rate_blog
        else:
            rate_blog = {'count': 0, 'rate': 0}
            return rate_blog

        return data

    def get_context_data(self, **kwargs):
        contaxt = super(Detail_weblog, self).get_context_data()
        category = self.object.category_web_model.first()
        recently = web_log.objects.filter(category_web_model=category).order_by('date')[:4]
        comment = Web_log_Comment.objects.filter(article_id=self.object.id, parent=None).order_by('-create_date')
        count_comment = Web_log_Comment.objects.filter(article_id=self.object.id).count()
        rate = self.rate_of_blog(self.object.id)

        contaxt['rate'] = rate
        contaxt['suggest'] = recently
        contaxt['comment'] = comment
        contaxt['count_comment'] = count_comment

        return contaxt

    def get_queryset(self):
        data = super(Detail_weblog, self).get_queryset()
        fillter = data.filter(slug=self.kwargs['slug']).first()
        try:
            auter_id = fillter.auter.id
        except:
            auter_id = ' '
        if self.request.user.id == auter_id:
            data = data.filter()
        else:
            data = data.filter(is_delete=False, is_active=True)
        return data


class comment(View):
    def get(self, request, *args, **kwargs):
        mymessage = request.GET.get('comment_mesage')
        id_of_web = request.GET.get('id_Weblog')
        parent = request.GET.get('parent')

        comment_web = Web_log_Comment.objects.create(article_id=id_of_web, user_id=request.user.id, text=mymessage,
                                                     parent_id=parent)
        comment_web.save()
        comments = Web_log_Comment.objects.filter(article_id=id_of_web, parent=None).order_by('-create_date')
        count_comment = Web_log_Comment.objects.filter(article_id=id_of_web).count()
        context = {'comment': comments, 'count_comment': count_comment}
        return render(request, 'comment/commentpartial.html', context)


@login_required(login_url='log_in')
def Make_weblog(request):
    if request.user.is_active and request.user.phone is not None:
        myform = Make_Weblog(request.POST, request.FILES)
        section2_form = Make_Weblog_section2(request.POST, request.FILES)
        section3_form = Make_Weblog_section3(request.POST, request.FILES)
        section4_form = Make_Weblog_section4(request.POST, request.FILES)
        sitesetting = photo_page.objects.first()

        context = {'form': myform, 'formsection2': section2_form,
                   'formsection3': section3_form, 'formsection4': section4_form, 'sitesetting': sitesetting}

        if request.method == 'POST':
            if myform.is_valid():
                main_title_f = myform.cleaned_data['title_main_f']
                short_discription = myform.cleaned_data['short_discription']
                category = myform.cleaned_data['category']
                genre = myform.cleaned_data['genre']
                tag_list = myform.cleaned_data['list_tag']
                main_photo = myform.cleaned_data['img1']
                main_title = myform.cleaned_data['title_main']
                main_story = myform.cleaned_data['main_text_story']
                img2 = myform.cleaned_data['img2']
                tag_id = []
                for addtag in tag_list:
                    newtag, boolval = Tag.objects.get_or_create(title=addtag)
                    tag_id.append(newtag.id)
                blog_creat = web_log.objects.create(title=main_title_f, shortdescription=short_discription,
                                                    gender=genre, main_title=main_title, discription=main_story,
                                                    main_photo=main_photo,
                                                    auter_id=request.user.id)

                setcat = [category]
                blog_creat.category_web_model.set(setcat)
                blog_creat.tag.set(tag_id)
                gallery = Gallery.objects.create(title=main_title_f, image1=img2)

                if section2_form.is_valid():
                    title_section_2 = section2_form.cleaned_data['title_section_2']
                    section_2_text_story = section2_form.cleaned_data['section_2_text_story']
                    img3 = section2_form.cleaned_data['img3']
                    other_section = more_discription.objects.create(title_seasionone=title_section_2,
                                                                    discription_seasionone=section_2_text_story)

                    gallery.image2 = img3
                    # Gallery.objects.update(image2=img3)

                    if section3_form.is_valid():
                        title_section_3 = section3_form.cleaned_data['title_section_3']
                        section_3_text_story = section3_form.cleaned_data['section_3_text_story']
                        img4 = section3_form.cleaned_data['img4']
                        more_discription.objects.filter(pk=other_section.id).update(title_seasiontwo=title_section_3,
                                                                                    discription_seasiontwo=section_3_text_story)
                        gallery.image3 = img4

                        if section4_form.is_valid():
                            title_section_4 = section4_form.cleaned_data['title_section_4']
                            section_4_text_story = section4_form.cleaned_data['section_4_text_story']
                            img5 = section4_form.cleaned_data['img5']
                            more_discription.objects.filter(pk=other_section.id).update(
                                title_seasiontree=title_section_4,
                                discription_seasiontree=section_4_text_story)
                            gallery.image4 = img5
                    gallery.save()
                    blog_creat.extra_discription = other_section
                blog_creat.gallery = gallery
                blog_creat.save()

                return redirect('Wait_Profile')
        return render(request, 'Make_Blog/make_blog.html', context)
    else:
        return redirect('log_in')


class Edit_weblog(UpdateView):
    model = web_log
    template_name = 'Make_Blog/Edit_blog.html'
    success_url = reverse_lazy('Wait_Profile')
    form_class = Edit_Form
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super(Edit_weblog, self).get_context_data()
        context['form1'] = Edit_form_img(self.request.POST, self.request.FILES, instance=self.object.gallery)
        context['form2'] = Edit_form_extra(self.request.POST or None, instance=self.object.extra_discription)

        return context

    def post(self, request, *args, **kwargs):
        post = super(Edit_weblog, self).post(request)
        title_seasionone = request.POST.get('title_seasionone')
        discription_seasionone = request.POST.get('discription_seasionone')
        title_seasiontwo = request.POST.get('title_seasiontwo')
        discription_seasiontwo = request.POST.get('discription_seasiontwo')
        title_seasiontree = request.POST.get('title_seasiontree')
        discription_seasiontree = request.POST.get('discription_seasiontree')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        if self.object.gallery is None:
            new = Gallery.objects.create(title=self.object.title)
            save_extra_db = web_log.objects.filter(pk=self.object.id).update(gallery=new)

        if image1 is not None:
            save_gallery = Gallery.objects.filter(pk=self.object.gallery.id).first()
            save_gallery.image1 = image1
            save_gallery.save()
        if image2 is not None:
            save_gallery = Gallery.objects.filter(pk=self.object.gallery.id).first()
            save_gallery.image2 = image2
            save_gallery.save()
        if image3 is not None:
            save_gallery = Gallery.objects.filter(pk=self.object.gallery.id).first()
            save_gallery.image3 = image3
            save_gallery.save()
        if image4 is not None:
            save_gallery = Gallery.objects.filter(pk=self.object.gallery.id).first()
            save_gallery.image4 = image4
            save_gallery.save()
        if self.object.extra_discription is not None:
            save_extra = more_discription.objects.filter(pk=self.object.extra_discription.id).update(
                title_seasionone=title_seasionone, discription_seasionone=discription_seasionone,
                title_seasiontwo=title_seasiontwo, discription_seasiontwo=discription_seasiontwo,
                title_seasiontree=title_seasiontree, discription_seasiontree=discription_seasiontree)
        else:
            if len(title_seasionone) > 3 or len(discription_seasionone) > 10:
                save_extra = more_discription.objects.create(title_seasionone=title_seasionone,
                                                             discription_seasionone=discription_seasionone,
                                                             title_seasiontwo=title_seasiontwo,
                                                             discription_seasiontwo=discription_seasiontwo,
                                                             title_seasiontree=title_seasiontree,
                                                             discription_seasiontree=discription_seasiontree)
                save_extra_db = web_log.objects.filter(pk=self.object.id).update(extra_discription=save_extra)
        return post

    def get_success_url(self):
        success = super(Edit_weblog, self).get_success_url()
        new = web_log.objects.filter(pk=self.object.id).update(is_active=False)
        return success

    def get_queryset(self):
        data = super(Edit_weblog,self).get_queryset()
        fillter = data.filter(pk=self.kwargs['pk']).first()
        try:
            auter_id = fillter.auter.id
        except:
            auter_id = ' '
        if self.request.user.id == auter_id:
            data = data.filter()
        else:
            data = data.filter(is_delete=False, is_active=True)
        return data


class add_rate(View):
    def rate_of_blog(self, web_log_id):
        myobject = Rate_of_Blog.objects.filter(weblod_id=web_log_id).all()
        count = myobject.count()
        sumscore = myobject.aggregate(Sum('score'))
        if count and sumscore is not None:
            rate_blog = {'count': count, 'rate': int((sumscore['score__sum'] / count) * 20)}
            addscore_to_detail = web_log.objects.filter(id=web_log_id).first()
            addscore_to_detail.satisfaction_percentage = rate_blog['rate']
            addscore_to_detail.save()
            return rate_blog
        else:
            rate_blog = {'count': 0, 'rate': 0}
            return rate_blog

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            weblogid = request.GET.get('weblog_id')
            userid = request.GET.get('user')
            rate = request.GET.get('rate')
            creat_rate, boo_rate = Rate_of_Blog.objects.update_or_create(weblod_id=weblogid, user_id=userid)
            creat_rate.score = rate
            creat_rate.save()

            context = {'rate': self.rate_of_blog(weblogid), 'res': 'Thank you for Score'}

            return render(request, 'detail_view/rate_ajax.html', context)
        else:
            return HttpResponse('First Log in after that select')




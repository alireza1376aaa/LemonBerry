from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers
from User_Setting.models import autentication
from User_Setting.send_email import send_email
from WebLog.models import web_log, more_discription, Gallery, Category_web, Gender, Tag, Rate_of_Blog, Web_log_Comment
from WebLogSetting.models import Contact_Us


# region auth /////////////////////////////////////////

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = autentication
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'main_location', 'location', 'phone',
                  'date_birth', 'about_user', 'is_verify', 'image_pro']


class register_new_user(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, min_length=7, write_only=True)
    repeat_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = autentication.objects.filter(username=attrs['username']).exists()
        email = autentication.objects.filter(email=attrs['email']).exists()
        password = attrs['password']
        repeat_pass = attrs['repeat_password']
        if username:
            raise serializers.ValidationError('this is username exists ')
        if email:
            raise serializers.ValidationError('this is email exists ')
        if password != repeat_pass:
            raise serializers.ValidationError('password is not same')
        return super(register_new_user, self).validate(attrs)

    def create(self, validated_data):
        new_user = autentication.objects.create(username=validated_data['username'], email=validated_data['email'],
                                                verify_code=get_random_string(99), is_verify=False)
        new_user.set_password(validated_data['password'])
        new_user.save()
        send_email('verify Account', new_user.email, {'user': new_user}, 'email/send_email.html')

        return new_user


class forget_password_api(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)

    def validate(self, attrs):
        email = autentication.objects.filter(email=attrs['email']).exists()
        if email == False:
            raise serializers.ValidationError('This email is not register')
        else:
            return super(forget_password_api, self).validate(attrs)

    def change(self):
        user = autentication.objects.filter(email=self.data['email']).first()
        send_email('verify Account', user.email, {'user': user}, 'email/send_email_password.html')


class edit_user_api(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    main_location = serializers.CharField(allow_null=True, required=False, max_length=100)
    location = serializers.CharField(allow_null=True, required=False, max_length=300)
    email = serializers.EmailField(required=True, max_length=100)
    phone = serializers.CharField(required=True, max_length=11)
    date_birth = serializers.DateField(allow_null=True, required=False)
    about_user = serializers.CharField(allow_null=True, required=False)
    image_pro = serializers.ImageField(allow_null=True, required=False)

    def validate(self, attrs):
        username = autentication.objects.filter(username=attrs['username'])
        email = autentication.objects.filter(email=attrs['email'])
        phone = autentication.objects.filter(phone=attrs['phone'])
        image = attrs['image_pro']

        if username.exists() and username.first().username != self.instance.username:
            raise serializers.ValidationError('this is username exists ')
        if email.exists() and email.first().email != self.instance.email:
            raise serializers.ValidationError('this is email exists ')
        if phone.exists() and phone.first().phone != self.instance.phone:
            raise serializers.ValidationError('this is phone exists ')
        if image is not None and image.size > 5000000:
            raise serializers.ValidationError('this file more than 5mb')

        return super(edit_user_api, self).validate(attrs)

    def update(self, instance, validated_data):
        update_user = autentication.objects.get(pk=instance.id)
        update_user.username = validated_data['username']
        update_user.first_name = validated_data['first_name']
        update_user.last_name = validated_data['last_name']
        update_user.main_location = validated_data['main_location']
        update_user.location = validated_data['location']
        update_user.email = validated_data['email']
        update_user.phone = validated_data['phone']
        update_user.date_birth = validated_data['date_birth']
        update_user.about_user = validated_data['about_user']
        if validated_data['image_pro'] is not None:
            update_user.image_pro = validated_data['image_pro']
        update_user.save()
        return update_user


class wait_Profile_ser(serializers.ModelSerializer):
    class Meta:
        model = web_log
        fields = ['title', 'date', 'satisfaction_percentage', 'is_active', 'is_delete']


class tiket_Profile_ser(serializers.ModelSerializer):
    class Meta:
        model = Contact_Us
        fields = ['Subject', 'Text_massage', 'response', 'visited']
        read_only_fields = ['Subject', 'Text_massage', 'visited']


class send_ticket(serializers.ModelSerializer):
    class Meta:
        model = Contact_Us
        fields = ['Subject', 'Text_massage']


# endregion

# region weblog /////////////////////////////////////////
class gallery_set(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['image1', 'image2', 'image3', 'image4']


class category_set(serializers.ModelSerializer):
    class Meta:
        model = Category_web
        fields = ['id', 'parent', 'title', 'is_active']


class gender_set(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['title', 'is_active']


class More_Discription(serializers.ModelSerializer):
    class Meta:
        model = more_discription
        fields = ['title_seasionone', 'discription_seasionone', 'title_seasiontwo', 'discription_seasiontwo',
                  'title_seasiontree', 'discription_seasiontree']


class Tag_set(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class weblog_complete(serializers.ModelSerializer):
    category_web_model = category_set(many=True)
    gallery = gallery_set()
    gender = gender_set()
    extra_discription = More_Discription()
    tag = Tag_set(read_only=True, many=True)

    class Meta:
        model = web_log
        fields = ['title', 'main_title', 'shortdescription', 'discription', 'extra_discription', 'date', 'main_photo',
                  'auter', 'category_web_model', 'gender', 'tag', 'gallery', 'satisfaction_percentage']


class list_weblog_short(serializers.ModelSerializer):
    category_web_model = category_set(read_only=True, many=True)

    class Meta:
        model = web_log
        fields = ['title', 'shortdescription', 'date', 'main_photo', 'category_web_model']


class edit_weblog(serializers.ModelSerializer):
    extra_discription = More_Discription()
    gallery = gallery_set()

    class Meta:
        model = web_log
        fields = ['title', 'main_title', 'shortdescription', 'discription', 'extra_discription', 'main_photo',
                  'gallery', 'category_web_model', 'gender']

    def validate(self, attrs):
        main_photo = attrs['main_photo']
        if main_photo is not None and main_photo.size > 5000000:
            raise serializers.ValidationError('main photo more than 5mb')

        gallery = attrs['gallery']
        image1 = gallery['image1']
        if image1 is not None and image1.size > 5000000:
            raise serializers.ValidationError('image1 more than 5mb')

        image2 = gallery['image2']
        if image2 is not None and image2.size > 5000000:
            raise serializers.ValidationError('image2 more than 5mb')

        image3 = gallery['image3']
        if image3 is not None and image3.size > 5000000:
            raise serializers.ValidationError('image3 more than 5mb')

        image4 = gallery['image4']
        if image4 is not None and image4.size > 5000000:
            raise serializers.ValidationError('image5 more than 5mb')

        return super(edit_weblog, self).validate(attrs)

    def update(self, instance, validated_data):
        extra_discription_data = validated_data.pop('extra_discription')
        extra_discription = instance.extra_discription
        if len(extra_discription_data['title_seasionone']) > 0 or len(
                extra_discription_data['title_seasiontwo']) > 0 or len(extra_discription_data['title_seasiontree']) > 0:
            if extra_discription is None:
                new_extra = more_discription.objects.create()
                extra_discription = new_extra
                instance.extra_discription = extra_discription
            for k, v in extra_discription_data.items():
                setattr(extra_discription, k, v)
            extra_discription.save()

        # ////////////////////////////////////////////////////////////////////
        gallery_data = validated_data.pop('gallery')
        gallery = instance.gallery
        if gallery_data['image1'] is not None:
            if gallery is None:
                new_gallery = Gallery.objects.create(title=str(instance.id))
                gallery = new_gallery
                instance.gallery = gallery
            for k, v in gallery_data.items():
                if v is not None:
                    setattr(gallery, k, v)
            gallery.save()

        instance.title = validated_data.get('title', instance.title)
        instance.main_title = validated_data.get('main_title', instance.main_title)
        instance.shortdescription = validated_data.get('shortdescription', instance.shortdescription)
        instance.discription = validated_data.get('discription', instance.discription)
        if validated_data.get('main_photo') is not None:
            instance.main_photo = validated_data.get('main_photo', instance.main_photo)
        cat_list = validated_data.pop('category_web_model')
        instance.category_web_model.set(cat_list)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance


class make_weblog(serializers.ModelSerializer):
    extra_discription = More_Discription()
    gallery = gallery_set()
    main_title = serializers.CharField(required=True)
    main_photo = serializers.ImageField(required=True)

    # gender = serializers.ChoiceField(required=True, choices=Gender.objects.all())
    # category_web_model = serializers.ChoiceField(required=True, choices=Category_web.objects.all())

    class Meta:
        model = web_log
        fields = ['title', 'category_web_model', 'gender', 'shortdescription', 'main_photo', 'main_title',
                  'discription', 'extra_discription', 'gallery']

    def validate(self, attrs):
        cat = attrs['category_web_model']
        if len(cat) > 1:
            if len(cat) < 0:
                raise serializers.ValidationError('category may not be blank.')
            else:
                raise serializers.ValidationError('You must select one category.')

        gender = attrs['gender']
        if gender is None:
            raise serializers.ValidationError('gender may not be blank.')

        main_photo = attrs['main_photo']
        if main_photo is None:
            raise serializers.ValidationError('main photo may not be blank.')
        if main_photo is not None and main_photo.size > 5000000:
            raise serializers.ValidationError('main photo more than 5mb')

        gallery = attrs['gallery']
        image1 = gallery['image1']
        if image1 is None:
            raise serializers.ValidationError('image1 may not be blank.')

        if image1 is not None and image1.size > 5000000:
            raise serializers.ValidationError('image1 more than 5mb')

        image2 = gallery['image2']
        if image2 is not None and image2.size > 5000000:
            raise serializers.ValidationError('image2 more than 5mb')

        image3 = gallery['image3']
        if image3 is not None and image3.size > 5000000:
            raise serializers.ValidationError('image3 more than 5mb')

        image4 = gallery['image4']
        if image4 is not None and image4.size > 5000000:
            raise serializers.ValidationError('image5 more than 5mb')

        return super(make_weblog, self).validate(attrs)

    @transaction.atomic
    def create(self, validated_data):

        extra_discription_data = validated_data.pop('extra_discription')
        gallery_data = validated_data.pop('gallery')
        newtitle = validated_data.pop('title')

        new_extra = None
        new_gallery = None
        if extra_discription_data is not None and len(extra_discription_data['title_seasionone']) > 0:
            new_extra = more_discription.objects.create()
            for k, v in extra_discription_data.items():
                if v is not None:
                    setattr(new_extra, k, v)
            new_extra.save()

        if gallery_data['image1'] is not None:
            new_gallery = Gallery.objects.create(title=newtitle)
            for k, v in gallery_data.items():
                if v is not None:
                    setattr(new_gallery, k, v)
            new_gallery.save()
        make_blog_new = web_log.objects.create(auter_id=self.context['request'].user.id)
        make_blog_new.title = newtitle
        x = validated_data.pop('category_web_model')
        # y = [x]
        make_blog_new.category_web_model.set(x)
        make_blog_new.gender = validated_data.pop('gender')
        make_blog_new.shortdescription = validated_data.pop('shortdescription')
        make_blog_new.main_photo = validated_data.pop('main_photo')
        make_blog_new.main_title = validated_data.pop('main_title')
        make_blog_new.discription = validated_data.pop('discription')
        if new_extra is not None:
            make_blog_new.extra_discription = new_extra

        if new_gallery is not None:
            make_blog_new.gallery = new_gallery
        make_blog_new.save()
        return make_blog_new


class addrate_serializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=0, max_value=5, required=True)

    class Meta:
        model = Rate_of_Blog
        fields = ['score']

    def create(self, validated_data):
        blog_id_seri = validated_data.pop('log_id')
        user_id_seri = validated_data.pop('user')
        newscore = validated_data.pop('score')
        web_logs = web_log.objects.filter(pk=blog_id_seri)
        RATE = Rate_of_Blog.objects.filter(weblod=web_logs.first(), user_id=user_id_seri.id)
        if RATE.exists():
            RATE.update(score=newscore)
            web_logs.update(satisfaction_percentage=newscore)
            return RATE.first()
        else:
            newRATE = Rate_of_Blog.objects.create(weblod=web_logs.first(), user_id=user_id_seri.id, score=newscore)
            web_logs.update(satisfaction_percentage=newscore)
            return newRATE


class addcomment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Web_log_Comment
        fields = ['id', 'article', 'parent', 'text']
        read_only_fields = ['id', 'article']

    def create(self, validated_data):
        blog_id_seri = validated_data.pop('log_id')
        user_id_seri = validated_data.pop('user')
        newcoment = validated_data.pop('text')
        parent = validated_data.pop('parent', None)
        if parent is None:
            Comment = Web_log_Comment.objects.create(article_id=blog_id_seri, user_id=user_id_seri.id, text=newcoment,
                                                     parent_id='')
        else:
            checkcomment = Web_log_Comment.objects.filter(article_id=blog_id_seri).all()
            cx = []
            for x in checkcomment:
                cx.append(x.id)
            if parent.id in cx:
                Comment = Web_log_Comment.objects.create(article_id=blog_id_seri, user_id=user_id_seri.id,
                                                         text=newcoment,
                                                         parent_id=parent.id)
            else:
                raise serializers.ValidationError('this comment you reply is empty')

        return Comment
# endregion

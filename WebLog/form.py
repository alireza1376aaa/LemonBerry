from django import forms
from django.core.exceptions import ValidationError

from Web_inher.models import Category_web, Gender


class Make_Weblog(forms.Form):
    Choice_cat = (('', 'Select your option'),)
    cate_model = Category_web.objects.filter(is_active=True)
    for x in cate_model:
        Choice_cat += ((x.id, x.title),)

    title_main_f = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Main Title', 'class': 'main_title', 'maxlength': '99'}),
        required=True, error_messages={'required': ''})

    short_discription = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '30', 'rows': '10', 'placeholder': 'Write a summary of your story', 'class': 'sh_dis',
               'maxlength': '480'}),
        required=True, error_messages={'required': ''})

    category = forms.ChoiceField(required=True, error_messages={'required': ''}, choices=Choice_cat,
                                 widget=forms.Select(
                                     attrs={'class': 'w-75', 'id': 'category', 'aria-label': 'Large select example'}))

    genre = forms.ModelChoiceField(queryset=Gender.objects.all(), required=True, error_messages={'required': ''},
                                   empty_label='Select your option',
                                   widget=forms.Select(
                                       attrs={'class': 'w-75', 'id': 'genre',
                                              'aria-label': 'Large select example'}))

    list_tag = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'list_tag'}))

    img1 = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'file-upload', 'onchange': "showMyImage(this,'#label-file-upload','#file-upload')",
               'accept': "image/jpeg, image/png"}), required=True, error_messages={'required': ''})

    title_main = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add Title of Story', 'class': 'main_title', 'maxlength': '99'}),
        required=True, error_messages={'required': ''})
    main_text_story = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '30', 'rows': '20', 'placeholder': 'Add Your Story', 'class': 'text_story_'}),
        required=True, error_messages={'required': ''})

    img2 = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'file-upload_1', 'onchange': "showMyImage(this,'#label-file-upload_1','#file-upload_1')",
               'accept': "image/jpeg, image/png"}), required=True, error_messages={'required': ''})

    def clean_category(self):
        myvalue = self.cleaned_data['category']
        return int(myvalue)

    def clean_list_tag(self):
        myvalue = self.cleaned_data['list_tag']
        return myvalue.split(',')

    def clean_title_main_f(self):
        myvalue = self.cleaned_data['title_main_f']

        if len(myvalue) > 3 and len(myvalue) < 100:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_short_discription(self):
        myvalue = self.cleaned_data['short_discription']
        if len(myvalue) > 20 and len(myvalue) < 500:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_title_main(self):
        myvalue = self.cleaned_data['title_main']

        if len(myvalue) > 3 and len(myvalue) < 100:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_main_text_story(self):
        myvalue = self.cleaned_data['main_text_story']

        if len(myvalue) > 30:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_img1(self):
        myvalue = self.cleaned_data['img1']
        if myvalue.size > 5000000:
            raise ValidationError('size photo more than 5mb')
        else:
            return myvalue

    def clean_img2(self):
        myvalue = self.cleaned_data['img2']
        if myvalue.size > 5000000:
            raise ValidationError('size photo more than 5mb')
        else:
            return myvalue


class Make_Weblog_section2(forms.Form):
    title_section_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add Title Section 2', 'class': 'main_title', 'maxlength': '99'}),
        required=False)
    section_2_text_story = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '30', 'rows': '20', 'placeholder': 'Continue Your Story', 'class': 'text_story_'}),
        required=False
    )
    img3 = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'file-upload_2', 'onchange': "showMyImage(this,'#label-file-upload_2','#file-upload_2')",
               'accept': "image/jpeg, image/png"}), required=False)

    def clean_title_section_2(self):
        myvalue = self.cleaned_data['title_section_2']

        if len(myvalue) > 1 and len(myvalue) < 100:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_section_2_text_story(self):
        myvalue = self.cleaned_data['section_2_text_story']

        if len(myvalue) > 1:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_img3(self):
        myvalue = self.cleaned_data['img3']
        if myvalue != None:
            if myvalue.size > 5000000:
                raise ValidationError('size photo more than 5mb')
            else:
                return myvalue


class Make_Weblog_section3(forms.Form):
    title_section_3 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add Title Section 3', 'class': 'main_title', 'maxlength': '99'}),
        required=False)
    section_3_text_story = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '30', 'rows': '20', 'placeholder': 'Continue Your Story', 'class': 'text_story_'}),
        required=False
    )
    img4 = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'file-upload_3', 'onchange': "showMyImage(this,'#label-file-upload_3','#file-upload_3')",
               'accept': "image/jpeg, image/png"}), required=False)

    def clean_title_section_3(self):
        myvalue = self.cleaned_data['title_section_3']

        if len(myvalue) > 1 and len(myvalue) < 100:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_section_3_text_story(self):
        myvalue = self.cleaned_data['section_3_text_story']

        if len(myvalue) > 1:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_img3(self):
        myvalue = self.cleaned_data['img4']
        if myvalue != None:
            if myvalue.size > 5000000:
                raise ValidationError('size photo more than 5mb')
            else:
                return myvalue


class Make_Weblog_section4(forms.Form):
    title_section_4 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add Title Section 4', 'class': 'main_title', 'maxlength': '99'}),
        required=False)
    section_4_text_story = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '30', 'rows': '20', 'placeholder': 'Continue Your Story', 'class': 'text_story_'}),
        required=False
    )
    img5 = forms.FileField(widget=forms.FileInput(
        attrs={'id': 'file-upload_4', 'onchange': "showMyImage(this,'#label-file-upload_4','#file-upload_4')",
               'accept': "image/jpeg, image/png"}), required=False)

    def clean_title_section_4(self):
        myvalue = self.cleaned_data['title_section_4']

        if len(myvalue) > 1 and len(myvalue)<100:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_section_4_text_story(self):
        myvalue = self.cleaned_data['section_4_text_story']

        if len(myvalue) > 1:
            return myvalue
        else:
            raise ValidationError(f'You must More than {len(myvalue)} character ')

    def clean_img3(self):
        myvalue = self.cleaned_data['img5']
        if myvalue != None:
            if myvalue.size > 5000000:
                raise ValidationError('size photo more than 5mb')
            else:
                return myvalue

from django import forms
from django.core.exceptions import ValidationError
from Web_inher.models import Gallery
from WebLog.models import web_log, more_discription
from Web_inher.models import Category_web, Gender


# class UserModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.id


class Edit_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Edit_Form, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = None
        self.fields['gender'].initial = 'salam'

    class Meta:
        model = web_log
        fields = ['title', 'gender', 'shortdescription', 'main_title', 'discription',
                  'main_photo', 'category_web_model']


        widgets = {
            'title': forms.TextInput(attrs={'class': 'main_title'}),
            'gender': forms.Select(attrs={'class': 'w-75', 'id': 'id_gender'}),
            'shortdescription': forms.Textarea(
                attrs={'cols': '30', 'rows': '10', 'class': 'sh_dis', 'maxlength': '480'}),
            'main_title': forms.TextInput(
                attrs={'placeholder': 'Add Title of Story', 'class': 'main_title', 'maxlength': '99'}),
            'discription': forms.Textarea(attrs={'cols': '30', 'rows': '20', 'class': 'text_story_'}),
            'main_photo': forms.FileInput(
                attrs={'id': 'file-upload', 'onchange': "showMyImage(this,'#label-file-upload','#file-upload')",
                       'accept': "image/jpeg, image/png"}),
            'category_web_model': forms.SelectMultiple(
                attrs={'class': 'w-75', 'aria-describedby': 'id_category_web_model_helptext',
                       'id': 'category'})
        }


class Edit_form_img(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image1', 'image2', 'image3', 'image4']
        widgets = {
            'image1': forms.FileInput(
                attrs={'id': 'file-upload_1', 'onchange': "showMyImage(this,'#label-file-upload_1','#file-upload')",
                       'accept': "image/jpeg, image/png"}),
            'image2': forms.FileInput(
                attrs={'id': 'file-upload_2', 'onchange': "showMyImage(this,'#label-file-upload_2','#file-upload')",
                       'accept': "image/jpeg, image/png"}),
            'image3': forms.FileInput(
                attrs={'id': 'file-upload_3', 'onchange': "showMyImage(this,'#label-file-upload_3','#file-upload')",
                       'accept': "image/jpeg, image/png"}),
            'image4': forms.FileInput(
                attrs={'id': 'file-upload_4', 'onchange': "showMyImage(this,'#label-file-upload_4','#file-upload')",
                       'accept': "image/jpeg, image/png"}),
        }


class Edit_form_extra(forms.ModelForm):
    class Meta:
        model = more_discription
        fields = ['title_seasionone', 'discription_seasionone', 'title_seasiontwo', 'discription_seasiontwo',
                  'title_seasiontree', 'discription_seasiontree']
        widgets = {
            'title_seasionone': forms.TextInput(attrs={'class': 'main_title'}),
            'discription_seasionone': forms.Textarea(attrs={'cols': '30', 'rows': '20', 'class': 'text_story_'}),
            'title_seasiontwo': forms.TextInput(attrs={'class': 'main_title'}),
            'discription_seasiontwo': forms.Textarea(attrs={'cols': '30', 'rows': '20', 'class': 'text_story_'}),
            'title_seasiontree': forms.TextInput(attrs={'class': 'main_title'}),
            'discription_seasiontree': forms.Textarea(attrs={'cols': '30', 'rows': '20', 'class': 'text_story_'}),

        }


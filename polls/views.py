from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib import messages
import re
# Create your views here.

def remove_spaces(string):
    pattern = r"[\s@&%^#]"
    return re.sub(pattern, "", string)
def Photo(request, img_pro):
    img_pro.name = f'{request.user.first_name}+{get_random_string(9)}.jpg'
    if img_pro.size > 5000000:
        messages.error(request, "more than 5MB")
        return img_pro


# def calculation_rate(asd):
#     myobject = Rate_of_Blog.objects.filter(weblog_id=1).count()
#     return myobject

from django.urls import path
from .views import (List_weblog, Detail_weblog, comment, Filter_web, Search_web,
                    Make_weblog, add_rate, Edit_weblog)

urlpatterns = [
    path('makeblog', Make_weblog, name='make_weblog'),
    path('list/<str:category>', List_weblog.as_view(), name='list_weblog'),
    path('list/<str:category>/filter', Filter_web.as_view()),
    path('list/<str:category>/addrate', add_rate.as_view()),
    path('list/<str:category>/search', Search_web.as_view()),
    path('list/<str:category>/<slug:slug>', Detail_weblog.as_view(), name='detail_weblog'),
    path('listcomment', comment.as_view(), name='comment_weblog'),
    path('edit/<pk>', Edit_weblog.as_view(), name='edit_weblog')

]

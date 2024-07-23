from django.urls import path
from .views import Log_in, panel_admin, Weblog_Admin, List_Blog_deactive, short_cut_active_delete, Show_blog_details, \
    active_or_deactive, List_Categoryh, change_cat, Add_category, List_Genre, change_gen, Add_genre, List_Blog_admin, \
    User_panel, List_user, Detail_user, Setting_panel, Get_img_page, Site_setting_page, About_setting_page, \
    Add_Employee_page, remove_Employee,Contact_admin_page,visited

urlpatterns = [
    path('log_in', Log_in.as_view()),
    path('admin_panel', panel_admin.as_view(), name='adminpanel'),
    # ////////////weblog////////////////////////////
    path('admin_panel/weblog', Weblog_Admin.as_view(), name='weblog_admin'),
    path('admin_panel/weblog/category', List_Categoryh.as_view(), name='list_category_add'),
    path('admin_panel/weblog/category/change', change_cat, name='change_cat_admin'),
    path('admin_panel/weblog/category/add', Add_category, name='add_cat_admin'),
    path('admin_panel/weblog/genre', List_Genre.as_view(), name='list_genre_add'),
    path('admin_panel/weblog/genre/change', change_gen, name='change_gen_admin'),
    path('admin_panel/weblog/genre/add', Add_genre, name='add_gen_admin'),
    path('admin_panel/weblog/list_deactiv_blog', List_Blog_deactive.as_view(), name='list_blog_deactive'),
    path('admin_panel/weblog/list_deactiv_blog/sh_ac_bl', short_cut_active_delete, name='sh_ac_bl'),
    path('admin_panel/weblog/list_deactiv_blog/act_deact', active_or_deactive, name='act_deact'),
    path('admin_panel/weblog/list_blog', List_Blog_admin.as_view(), name='list_blog_a'),
    path('admin_panel/weblog/list_blog/<a_blog_d>', Show_blog_details, name='blog_details_admin'),
    # /////////////user/////////////////////////////////
    path('admin_panel/user', User_panel.as_view(), name='user_panel'),
    path('admin_panel/user/list_user', List_user.as_view(), name='list_user_p'),
    path('admin_panel/user/list_visited', visited, name='visited'),
    path('admin_panel/user/list_user/<pk>', Detail_user.as_view(), name='details_user_p'),
    # //////////////setting///////////////////////////////
    path('admin_panel/setting', Setting_panel.as_view(), name='setting_panel'),
    path('admin_panel/setting/set_image', Get_img_page, name='image_set_page'),
    path('admin_panel/setting/site_setting', Site_setting_page, name='site_setting_page'),
    path('admin_panel/setting/about_us', About_setting_page, name='about_setting_page'),
    path('admin_panel/setting/employee', Add_Employee_page, name='add_employee_page'),
    path('admin_panel/setting/remove/<id_em>', remove_Employee, name='remove_employee'),
    path('admin_panel/setting/contact', Contact_admin_page, name='contact_admin_page'),

]

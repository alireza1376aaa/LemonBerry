from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Register_user,Verify_account,Log_in,forgot_pass_first,forgot_pass,edit_profile,Log_out,wait,ticket
urlpatterns = [
    path('register/', Register_user.as_view(),name='Register'),
    path('verify/<verifycode>',Verify_account,name='veryfy'),
    path('login',Log_in.as_view(),name='log_in'),
    path('logout',login_required(Log_out.as_view()) , name='Log_out'),
    path('forgot_pass',forgot_pass_first,name='forgot_pass'),
    path('forgetpass/<verifycode>',forgot_pass),
    path('edit_profile',edit_profile,name='Edit_Profile'),
    path('edit_profile/wait', wait.as_view(), name='Wait_Profile'),
    path('edit_profile/ticket', ticket.as_view(), name='Ticket_pro'),

]
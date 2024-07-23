from django.urls import path
from .views import (List_user, Details_user, register_api, edit_profile, Wait_profile, Tiket_profile, Send_Tiket,
                    Response_tiket, forgot_password, List_weblog_complete, List_weblog_short,
                    Details_weblog, Edit_weblog, category_set_read, category_edit, gender_set_read,
                    gender_edit, Makeblog, AddRate, AddComment)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('user/list_user', List_user.as_view(), name='list_user_api'),
    path('user/details_user/<pk>', Details_user.as_view(), name='details_user_api'),
    path('user/register', register_api.as_view(), name='register_api'),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/forgot_password', forgot_password.as_view(), name='forgot_password'),
    path('user/edit_profile/', edit_profile.as_view(), name='edit_pro_api'),
    path('user/wait_profile/', Wait_profile.as_view(), name='wait_profile'),
    path('user/tiket_profile/', Tiket_profile.as_view(), name='tiket_profile'),
    path('user/send_ticket/', Send_Tiket.as_view(), name='send_Tiket'),
    path('user/response_ticket/<pk>', Response_tiket.as_view(), name='response_tiket'),
    # /////////////////////////////////////////////////////////////////////////////////////////////
    path('web_log/list/complete', List_weblog_complete.as_view(), name='list_weblog_complete'),
    path('web_log/list', List_weblog_short.as_view(), name='list_weblog_short'),
    path('web_log/list/<pk>', Details_weblog.as_view(), name='details_weblog'),
    path('web_log/edit/<id>', Edit_weblog.as_view(), name='edit_weblog'),
    path('web_log/category', category_set_read.as_view(), name='category_weblog'),
    path('web_log/category/<pk>', category_edit.as_view(), name='category_edit_weblog'),
    path('web_log/gender', gender_set_read.as_view(), name='gender_weblog'),
    path('web_log/gender/<pk>', gender_edit.as_view(), name='gender_edit_weblog'),
    path('web_log/makeblog', Makeblog.as_view(), name='makeblog'),
    path('web_log/list/<pk>/rate', AddRate.as_view(), name='add_rate_weblog'),
    path('web_log/list/<pk>/comment', AddComment.as_view(), name='add_comment_weblog'),
    # /////////////////////////////////////////////////////////////////////////////////////////////
    path('doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

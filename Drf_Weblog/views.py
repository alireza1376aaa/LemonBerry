from rest_framework import generics, request, response, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from WebLog.models import web_log, Category_web, Gender, Web_log_Comment
from User_Setting.models import autentication
from WebLogSetting.models import Contact_Us
from .serializer import register_new_user, edit_user_api, wait_Profile_ser, tiket_Profile_ser, forget_password_api, \
    weblog_complete, list_weblog_short, edit_weblog, send_ticket, User_serializer, category_set, gender_set, \
    make_weblog, addrate_serializer, addcomment_serializer
from drf_spectacular.utils import extend_schema, extend_schema_view


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6


# region auth /////////////////////////////////////////

@extend_schema(
    summary='List All OF the User For Admin'
)
class List_user(generics.ListAPIView):
    queryset = autentication.objects.all()
    serializer_class = User_serializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAdminUser]


@extend_schema(
    summary='Details All OF the User For Admin'
)
class Details_user(generics.RetrieveAPIView):
    queryset = autentication.objects.all()
    serializer_class = User_serializer
    permission_classes = [IsAdminUser]


class register_api(generics.GenericAPIView):
    serializer_class = register_new_user

    @extend_schema(
        summary='Register User'
    )
    def post(self, request: request.Request):
        new_user = register_new_user(data=request.data)
        if new_user.is_valid():
            new_user.save()
            return response.Response(new_user.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


class forgot_password(generics.GenericAPIView):
    serializer_class = forget_password_api

    @extend_schema(
        summary='When Forget Password use this metod for send email'
    )
    def post(self, request: request.Request):
        new_user = self.serializer_class(data=request.data)
        if new_user.is_valid():
            new_user.change()
            data = new_user.data
            data['massage'] = 'send to your email'
            return response.Response(data=data, status=status.HTTP_200_OK)
        else:
            return response.Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


class edit_profile(generics.GenericAPIView):
    serializer_class = edit_user_api
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Show User Profile'
    )
    def get(self, request: request.Request):
        data = autentication.objects.filter(pk=request.user.id).first()
        if request.user.is_verify:
            serialize = edit_user_api(data)
            return response.Response(serialize.data, status=status.HTTP_200_OK)
        else:
            return response.Response({'massage': 'first you must active acount'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Edit User Profile'
    )
    def put(self, request: request.Request):
        data = autentication.objects.filter(pk=request.user.id).first()
        if request.user.is_verify:
            serialize = edit_user_api(data, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return response.Response(serialize.data, status=status.HTTP_202_ACCEPTED)
            else:
                return response.Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return response.Response({'massage': 'first you must active acount'}, status=status.HTTP_400_BAD_REQUEST)


class Wait_profile(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Show Blog User Status'
    )
    def get(self, request: request.Request):
        if request.user.is_verify and request.user.phone is not None:
            data = web_log.objects.filter(auter_id=request.user.id).all().order_by('-date')
            serializers = wait_Profile_ser(data, many=True)
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return response.Response({'massage': 'first you must active acount'}, status=status.HTTP_400_BAD_REQUEST)


class Tiket_profile(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Show Ticket User Status'
    )
    def get(self, request: request.Request):
        if request.user.is_verify:
            data = Contact_Us.objects.filter(User_id=request.user.id).all()
            serializers = tiket_Profile_ser(data, many=True)
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return response.Response({'massage': 'first you must active acount'}, status=status.HTTP_400_BAD_REQUEST)


class Send_Tiket(generics.GenericAPIView):
    queryset = Contact_Us
    serializer_class = send_ticket

    @extend_schema(
        summary='Send Tiket'
    )
    def post(self, request: request.Request):
        if request.user.is_verify:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(User=request.user)
                return response.Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'massage': 'first you must active acount'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary='Response to Tiket client'
)
class Response_tiket(generics.RetrieveUpdateAPIView):
    queryset = Contact_Us
    serializer_class = tiket_Profile_ser
    permission_classes = [IsAdminUser]


# endregion10


# region web_log ///////////////////////////////
@extend_schema(
    summary='List All Blog with all of the details'
)
class List_weblog_complete(generics.ListAPIView):
    queryset = web_log.objects
    serializer_class = weblog_complete
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = super(List_weblog_complete, self).get_queryset()
        newedata = data.filter(is_active=True)
        return newedata

@extend_schema(
    summary='List All Of the Blog'
)
class List_weblog_short(generics.ListAPIView):
    queryset = web_log.objects
    serializer_class = list_weblog_short
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        data = super(List_weblog_short, self).get_queryset()
        newedata = data.filter(is_active=True)
        return newedata

@extend_schema(
    summary='Details Blog'
)
class Details_weblog(generics.GenericAPIView):
    serializer_class = weblog_complete
    queryset = web_log.objects

    def get(self, request: request.Request, pk):
        datecheck = self.queryset.filter(pk=pk).first()
        try:
            auter_id = datecheck.auter.id
        except:
            auter_id = ' '
        if request.user.id == auter_id:
            data = self.queryset.filter(pk=pk).first()
        else:
            data = self.queryset.filter(pk=pk, is_delete=False, is_active=True).first()

        serialize = self.serializer_class(data)
        if data is None:
            return response.Response(None, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serialize.data, status=status.HTTP_200_OK)

@extend_schema(
    summary='Edit Blog'
)
class Edit_weblog(generics.RetrieveUpdateAPIView):
    queryset = web_log.objects
    serializer_class = edit_weblog
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data = super().get_queryset()
        x = data.filter(auter_id=self.request.user.id)
        return x

@extend_schema(
    summary='List Category'
)
class category_set_read(generics.ListAPIView):
    queryset = Category_web.objects.all()
    serializer_class = category_set

@extend_schema(
    summary='Edit Category for Admin'
)
class category_edit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category_web.objects.all()
    serializer_class = category_set
    permission_classes = [IsAdminUser]

@extend_schema(
    summary='List Gender'
)
class gender_set_read(generics.ListAPIView):
    queryset = Gender.objects.all()
    serializer_class = gender_set

@extend_schema(
    summary='Edit Gender for Admin'
)
class gender_edit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gender.objects.all()
    serializer_class = gender_set
    permission_classes = [IsAdminUser]

@extend_schema(
    summary='Make Blog'
)
class Makeblog(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = web_log.objects.all()
    serializer_class = make_weblog


class AddRate(generics.GenericAPIView):
    serializer_class = addrate_serializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Add Rate for Blog'
    )
    def post(self, request: Request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(log_id=pk, user=request.user)
            return response.Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AddComment(generics.GenericAPIView):
    queryset = Web_log_Comment.objects
    serializer_class = addcomment_serializer

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Show all Comment for the Blog'
    )
    def get(self, request: Request, pk):
        query = self.queryset.filter(article_id=pk).all()
        serializer = self.serializer_class(query, many=True)
        return response.Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        summary='Set Comment for the Blog'
    )
    def post(self, request: Request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(log_id=pk, user=request.user)
            return response.Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# endregion

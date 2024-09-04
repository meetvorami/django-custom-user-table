from django.urls import path

from app.views import CreateUser, GetAllUser, LoginUser, LogoutUser

urlpatterns = [
    path("create_user/", CreateUser.as_view(), name="createuser"),
    path("login/", LoginUser.as_view(), name="login_user"),
    path("logout/", LogoutUser.as_view(), name="logoutuser"),
    path("user_list/", GetAllUser.as_view(), name="get_all_user"),
]

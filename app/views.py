from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from app.services import UserManagement, UserManagementWithServices
from utils.responses import failure_response


@authentication_classes([])
class CreateUser(APIView):
    def post(self, request):
        if not request.data:
            return Response(
                failure_response(message="required data not passed"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return UserManagementWithServices().create_user(request)


@authentication_classes([])
class LoginUser(APIView):
    def post(self, request):
        if not request.data:
            return Response(
                failure_response(message="required data not passed"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return UserManagementWithServices().login_user(request)


class LogoutUser(APIView):
    def get(self, request):
        return UserManagementWithServices().logout()


class GetAllUser(APIView):
    def get(self, request):
        return UserManagement().get_all_user()

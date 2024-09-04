import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response

from app.models import CustomUser
from app.serializers import UserCrudSerializers
from utils.jwt_utils import TokenGenration
from utils.kafka_producer import KafkaProd
from utils.redis_utils import RedisClient
from utils.responses import failure_response, success_response


class UserManagement:
    def __init__(self):
        pass

    def get_all_user(self):
        serializer = UserCrudSerializers(CustomUser.objects.all(), many=True)
        return Response(
            success_response(data=serializer.data, message="User fetch succssfully."),
            status=status.HTTP_200_OK,
        )


class UserManagementWithServices:
    def __init__(self):
        self.token = TokenGenration()
        self.redis_client = RedisClient()
        self.kafka_prod = KafkaProd()

    def create_user(self, request):
        try:
            serializer = UserCrudSerializers(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                access_token = self.token.create_access_token({"sub": user.id})
                refresh_token = self.token.create_refresh_token({"sub": user.id})

                serializer = UserCrudSerializers(user)
                data = serializer.data

                #  store data to redis
                self.redis_client.set(
                    f"token:{user.email}",
                    json.dumps(
                        {"access_token": access_token, "refresh_token": refresh_token}
                    ),
                )

                data.update(
                    {"access_token": access_token, "refresh_token": refresh_token}
                )
                # send task to kafka
                self.kafka_prod.send_event({"user_email": f"{user.email}"})

                return Response(
                    success_response(
                        data=data, message="User created successfully.", status_code=201
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                failure_response(
                    message="required fields are incorrect", data=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                failure_response(
                    message="something went wrong", status_code=500, error=e
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def login_user(self, request):
        try:
            user = authenticate(
                request,
                email=request.data.get("email"),
                password=request.data.get("password"),
            )
            if not user:
                return Response(
                    failure_response(message="invalid login details"),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            access_token = self.token.create_access_token({"sub": user.id})
            refresh_token = self.token.create_refresh_token({"sub": user.id})
            serialzier = UserCrudSerializers(user)

            self.redis_client.set(
                f"token:{user.email}",
                json.dumps(
                    {"access_token": access_token, "refresh_token": refresh_token}
                ),
            )

            data = serialzier.data

            data.update({"access_token": access_token, "refresh_token": refresh_token})
            return Response(
                success_response(data=data, message="login successfull"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                failure_response(
                    message="something went wrong", status_code=500, error=e
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def logout(self, request):
        try:
            RedisClient().delete(f"token:{request.user.email}")
            return Response(
                success_response({}, message="User Logout Successfully"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                failure_response(
                    message="something went wrong", status_code=500, error=e
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

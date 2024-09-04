from rest_framework import serializers

from app.models import CustomUser


class UserCrudSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = CustomUser(email=validated_data.get("email"))
        user.set_password(validated_data.get("password"))
        user.save()
        return user

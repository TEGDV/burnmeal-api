from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    _password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # This is called when the serializer its invoked by POST Method
    def save(self):

        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )

        password = self.validated_data["password"]
        _password = self.validated_data["_password"]
        if not password == _password:
            raise serializers.ValidationError({"password": "Passwords must be match"})
        user.set_password(password)
        user.save()
        return user

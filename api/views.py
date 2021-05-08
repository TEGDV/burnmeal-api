from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from api.serializers import RegistrationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["POST"])
def registration(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
    data = dict()
    if serializer.is_valid():
        user = serializer.save()
        data["response"] = "Succesfully registered new user."
        data["email"] = user.email
        data["username"] = user.username
    else:
        data = serializer.errors
    return Response(data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def some_protected_view(request):
    data = {"message": "Si Jalo"}
    return Response(data)

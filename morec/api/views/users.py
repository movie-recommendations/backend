from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from api.serializers.users import UserVerifyEmailSerializer


@api_view(['POST'])
def user_verify_email(request):
    serializer = UserVerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

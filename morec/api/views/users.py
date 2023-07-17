from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers.users import UserVerifyEmailSerializer


@api_view(['POST'])
def user_verify_email(request):
    serializer = UserVerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

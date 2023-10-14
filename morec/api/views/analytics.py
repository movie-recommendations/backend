from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from analytics.model.inference import get_inference, user_processing

@api_view(['GET'])
@permission_classes([AllowAny])
def get_forecast(request):
    user = request.user
    inference = get_inference(
        user_processing(
            'b712b896-6090-49b9-8d8f-4874cbd4013d'
            #user.id
        )
    )

    return Response(inference)

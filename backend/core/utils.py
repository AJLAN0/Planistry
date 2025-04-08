from rest_framework.response import Response
from rest_framework import status

def create_response(data=None, message=None, success=True, status_code=status.HTTP_200_OK):
    response_data = {
        'success': success,
        'message': message,
        'data': data
    }
    return Response(response_data, status=status_code)
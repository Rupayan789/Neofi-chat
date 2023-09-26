from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from django.http import JsonResponse

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

        except Exception as e:
            # Handle the exception and send a custom response
            error_message = str(e)
            response = self.handle_exception(error_message)
        return response

    def handle_exception(self, error_message):
        # Create a custom JSON response for the error
        response_data = {
            'error': error_message,
        }
        print('error',response_data)
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

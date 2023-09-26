from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class HomeRoute(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        return Response("Server up and running",status=status.HTTP_200_OK)
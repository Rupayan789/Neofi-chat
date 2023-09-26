from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .utils import get_suggested_friends_list, get_target_user
from .models.message import Message
from django.core.serializers.json import DjangoJSONEncoder
import json
User = get_user_model()

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		print(request)
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response({'success': True}, status=status.HTTP_201_CREATED)
		return Response({'success':False},status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)

		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			print(user)
			if user:
				login(request, user)
				user.is_online = True
				user.save()
				return Response({'success': True}, status=status.HTTP_200_OK)
		return Response({'success':False},status=status.HTTP_400_BAD_REQUEST)
	

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	def post(self, request):
		user = request.user
		if request.user and not isinstance(request.user, AnonymousUser):
			user = request.user
			user.is_online = False
			user.save()
			logout(request)
			return Response({'success': True}, status=status.HTTP_200_OK)
		else:
			# Handle the case where the user is not authenticated or is an AnonymousUser
			return Response({'success':False}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		print(request)
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class SuggestedFriends(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		target_user = get_target_user(request.user)
		top_friends = get_suggested_friends_list(target_user)
		return Response({'users': top_friends,'success': True}, status=status.HTTP_200_OK)
	
class GetOnlineUsers(APIView):
	def get(self, request):
		users = User.objects.filter(is_online=True).values('user_id','email','username','is_online')
		return Response({'users': users, 'success': True}, status=status.HTTP_200_OK)
	
class StartChat(APIView):
	def post(self, request):
		try:
			data = request.data
			recipient = list(User.objects.filter(email=data['email']).values('user_id','email','username','is_online'))[0]

			print(recipient)
			if recipient and recipient['is_online']:
				other_user_id = recipient['user_id']
				my_id = request.user.user_id
				room_name = None
				if int(my_id) > int(other_user_id):
					room_name = f'{my_id}-{other_user_id}'
				else:
					room_name = f'{other_user_id}-{my_id}'
				messages = list(Message.last_50_messages(self,room_name=room_name))
				return Response({'success':True, 'message': 'User is online', 'data': messages}, status=status.HTTP_200_OK)
			else:
				return Response({'success':False,'message':"User is Offline",'data': None}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
				return Response({'success':False,'message':str(e),'data': None}, status=status.HTTP_400_BAD_REQUEST)

		
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,GenericAPIView,UpdateAPIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializer import UserRegistrationSerializer,UserLoginSerializer,ChangePasswordSerializer,LoginSerializer
from rest_framework import status
from .models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def home(request):
	return render(request,"home.html")

def signup(request):
	return render(request,"registration/signup.html")

def login(request):
	return render(request,"registration/login.html")

def retrieve(request):
	return render(request,"retrieve.html")

def update(request):
	return render(request,"update.html")

def delete(request):
	return render(request,"delete.html")

def newpassword(request):
	return render(request,"newpassword.html")

def passwordresetcomplete(request):
	return render(request,"password_reset_complete.html")

def passwordreset(request):
	return render(request,"password_reset.html")

def passwordresetform(request):
	return render(request,"password_reset_form.html")

def passwordresetemail(request):
	return render(request,"password_reset_sent.html")


class UserRegistrationView(CreateAPIView):
	serializer_class = UserRegistrationSerializer
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAdminUser]
	
	def post(self,request):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception =True)
		serializer.save()
		status_code = status.HTTP_201_CREATED
		response = {
			'success' : 'True',
			'status_code' : status_code,
			'message':'User Registered successfully',
			}

		return Response(response,status=status_code)


class UserLoginView(GenericAPIView):
	permission_classes =(AllowAny,)
	serializer_class = UserLoginSerializer

	def post(self,request):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception =True)

		
		status_code = status.HTTP_200_OK
		response = {
			'success' : 'True',
			'status_code' : status_code,
			'message':'User Logged in successfully',
			}

		return Response(response,status=status_code)


class ChangePasswordView(UpdateAPIView):
	queryset = User.objects.all()
	permission_classes = (IsAuthenticated,)
	serializer_class = ChangePasswordSerializer


class Update(UpdateAPIView):
	queryset = User.objects.all()
	serializer_class = LoginSerializer
	permission_classes = (IsAuthenticated,)


def mail(request):
	user = User.objects.get(email="jeminkukadia@gmail.com")
	subject = "Greetings"
	msg     = "Congratulations for your success"
	to      = user.email
	res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
	if(res == 1):
		msg = "Mail Sent Successfuly"
	else:
		msg = "Mail could not sent"
	return HttpResponse(msg)  


class sentMail(TemplateView):
	template_name = 'password_reset'

	def post(self, request, *args, **kwargs):
		email = self.request.POST.get("email")
		subject = "Greetings"
		msg     = "Congratulations for your success"
		to      = email
		res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
		if(res == 1):
			msg = "Mail Sent Successfuly"
		else:
			msg = "Mail could not sent"
		return HttpResponse(msg)  



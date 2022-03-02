from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TruckSerializer
from rest_framework.response import Response
from .models import Truck
import datetime,jwt
import os


# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            user = jwt.decode(token,os.environ['SECRET_HASH'],algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        data=self.formater(request.data,user)    
        serializer = TruckSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def formater(self,data,user):
            
            return{
                
                    "creator":user['id'],
                    "truckNo": data['truckNo'],
                    "password":data["password"],
            }



class LoginView(APIView):
    def post(self,request):
        truckNo = request.data['truckNo']
        password = request.data['password']

        user = Truck.objects.filter(truckNo = truckNo).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1440),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,os.environ['SECRET_HASH'],algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }

        return response        

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token,os.environ['SECRET_HASH'],algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Truck.objects.filter(id=payload['id']).first()
        serializer = TruckSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }
        return response     
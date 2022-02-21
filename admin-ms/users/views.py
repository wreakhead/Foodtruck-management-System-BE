from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
import datetime,jwt,os,requests,json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

class RegisterView(APIView):
    @csrf_exempt
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

class LoginView(APIView):
    @csrf_exempt
    def post(self,request):
        admin = request.data['admin']
        password = request.data['password']

        user = User.objects.filter(admin = admin).first()
        

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=int(os.environ['JWT_EXP'])),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,os.environ['SECRET_HASH'],algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key=os.environ['JWT_ALIAS'],value=token,httponly=True)
        response.data = {
            os.environ['JWT_ALIAS']:token,
            
        }

        return response


class AddTruck(APIView):
    @csrf_exempt
    def post(self,request):
        cookies = request.COOKIES
        token = request.COOKIES.get(os.environ['JWT_ALIAS'])
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            jwt.decode(token,os.environ['SECRET_HASH'],algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')    

        res = requests.post(os.environ['TRUCK_API']+"api/registertruck",cookies=cookies,data=request.data)
        jsonRes= json.loads(res.text)
        status = res.status_code 
        if res.status_code == requests.codes.ok:
            return Response(jsonRes,status=status)
        return Response({"message":jsonRes['truckNo']},status=status)    
     




class UserView(APIView):
    @csrf_exempt
    def get(self,request):
        token = request.COOKIES.get(os.environ['JWT_ALIAS'])

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token,os.environ['SECRET_HASH'],algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)


        return Response(serializer.data)

class LogoutView(APIView):
    @csrf_exempt
    def get(self,request):
        token = request.COOKIES.get(os.environ['JWT_ALIAS'])
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            jwt.decode(token,os.environ['SECRET_HASH'],algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        response = Response()
        response.delete_cookie(os.environ['JWT_ALIAS'])
        response.data={
            'message':'success'
        }
        return response                
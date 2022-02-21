
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','admin','domain','password']
        extra_kwargs = {
            'password':{
                'write_only':True #wont return password in json response
            }
        }
    def create(self, validated_data):
        
        password = validated_data.pop('password',None)  #taking out password 
        instance = self.Meta.model(**validated_data) #instance without password
        if password is not None:
            instance.set_password(password) #hashing password
        instance.save()
        return instance    

from django.forms import BooleanField, IntegerField
from rest_framework import serializers
from .models import Truck




class TruckSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Truck
        fields =  ['id','truckNo','creator','password','disabled']
        
        extra_kwargs = {
            'password':{
                'write_only':True #wont return password in json response
            },
           

        }
    def create(self, validated_data):
        
        password = validated_data.pop('password',None)  #taking out password 
        instance = self.Meta.model(**validated_data) #instance without password
        if password is not None:
            instance.set_password(password) #hashing password
        instance.save()
        return instance

    
    
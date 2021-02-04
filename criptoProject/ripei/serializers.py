from .models import UserProfile, Crito
from rest_framework import serializers
from django.contrib.auth.models import User



class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CritoSerializer(serializers.ModelSerializer):

    

    class Meta: 
        model = Crito
        fields = '__all__'

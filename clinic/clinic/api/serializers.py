from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from base import models

class Get_All_Doctors_Serializer(ModelSerializer):
    img_url = serializers.SerializerMethodField()

    def get_img_url(self,obj):
        return obj.img.url if obj.img else None

    class Meta:
        model = models.User
        fields = ['specialty','first_name','last_name','img_url','id']

class SimpleDoctorSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    def get_img_url(self,obj):
        return obj.img.url if obj.img else None
    class Meta:
        model = models.User
        fields = ['first_name','last_name', 'img_url','id']


class SimplePatientSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    def get_img_url(self,obj):
        return obj.img.url if obj.img else None
    
    class Meta:
        model = models.User
        fields = ['first_name','last_name', 'img_url','id'] 


class Get_Appointments_Serializer(ModelSerializer):
    doctor = SimpleDoctorSerializer(read_only=True)
    patient = SimplePatientSerializer(read_only=True)

    class Meta:
        model = models.Appointment
        fields = ['doctor','patient','status','confirmed_appointment_datetime','expected_appointment_date','id']
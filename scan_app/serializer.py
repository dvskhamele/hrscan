from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ApplicantCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantCV
        fields = '__all__'
        read_only = ['pk']

class ApplicantCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantCollege
        fields = '__all__'
        read_only = ['pk']

        #def get_queryset(self):
        #    return self.queryset.all()
            #.order_by('')

class ApplicantDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDegree
        fields = '__all__'
        read_only = ['pk']

class CVKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVKeywords
        fields = '__all__'
        read_only = ['pk']

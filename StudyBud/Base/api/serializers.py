from dataclasses import field
from rest_framework.serializers import ModelSerializer
from Base.models import Room

class Roomserializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
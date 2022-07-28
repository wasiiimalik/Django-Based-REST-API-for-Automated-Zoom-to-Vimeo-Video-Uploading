from models import *
from rest_framework import serializers

class ExceptionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = zoomwebhookdata
        fields = "__all__"
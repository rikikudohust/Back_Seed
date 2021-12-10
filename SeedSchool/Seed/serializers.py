from rest_framework import serializers
from .models import Menu
class MenuSerializer(serializers.ModelSerializers):
    class Meta:
        model = Menu
        fields = '__all__'

    


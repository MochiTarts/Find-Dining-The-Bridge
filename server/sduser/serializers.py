from rest_framework import serializers
from .models import SDUser
 
class SDUserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = SDUser
        fields = ('id', 'username', 'first_name', 'last_name',)

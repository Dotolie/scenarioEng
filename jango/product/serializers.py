from rest_framework import serializers
from .models import Item, MyModel

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")
        #fields = ('name', 'description', 'cost')
        
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ("__all__")
        #fields = ('name', 'description', 'cost')
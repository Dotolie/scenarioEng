from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import ItemSerializer, MyModelSerializer
from .models import Item
from .models import MyModel
from .engine import *

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    

class contentViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer





en = Engine()




@api_view(['GET'])
def loadScenarioFile(request):
    if request.query_params:
        filename = request.query_params.get('file', None)
        res = en.ReadScenario(filename)
        return res
    else:
        res = en.GetAllScenario()
        return res


@api_view(['GET'])
def readOneScenario(request, id):
    res = en.GetOneScenario(id)

    return res


@api_view(['GET'])
def readAllResult(request):
    res = en.GetAllResult()

    return res


@api_view(['GET'])
def readOneResult(request, id):
    res = en.GetOneResult(id)

    return res



@api_view(['GET'])
def readAllDevice(request):
    res = en.GetAllDevice()

    return res


@api_view(['GET'])
def testOne(request, id):
    res = en.TestOneStep(id)

    return res
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Toy
from .serializers import ToySerializer

class JSONResponse(HttpResponse):
    def _init_(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs["content-type"] = "application/json"
        super(JSONResponse, self)._init_(content, **kwargs)
@csrf_exempt
def toy_list(request):
        if request.method == 'GET':
            toys = Toy.objects.all()
            toys_serializer = ToySerializer(toys, many=True)
            return JSONResponse(toys_serializer.data)
        elif request.method == 'POST':
            toy_data = JSONParser().parse(request)
            toy_serializer = ToySerializer(data=toy_data)
            if toy_serializer.is_valid():
                toy_serializer.save()
            return JSONResponse(toy_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def toy_detail(request, pk):
        try:
            toy = Toy.objects.get(pk=pk)
        except Toy.DoesNotExist:
            return JSONResponse(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            toy_serializer = ToySerializer(toy)
            return JSONResponse(toy_serializer.data)
        elif request.method == 'DELETE':
            toy.delete()
            return JSONResponse(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            toy_data = JSONParser().parse(request)
            toy_serializer = ToySerializer(data=toy_data)
            if toy_serializer.is_valid():
                toy_serializer.save()
                return JSONResponse(toy_serializer.data)
            return JSONResponse(status=status.HTTP_404_NOT_FOUND)


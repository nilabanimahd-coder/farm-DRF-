from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import  FarmListSerializer,FarmDetaielSerializer,FieldSerializer
from .models import FarmModel,FieldModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

# Create your views here.
class FarmView(APIView):

    def get(self,request):
        farms=FarmModel.objects.all()
        ser=FarmListSerializer(farms,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    
    def post(self,reqest):
        ser=FarmListSerializer(data=reqest.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class FarmDetailView(APIView):

    def get(self,request,pk):
        farm=FarmModel.objects.get(id=pk)
        ser=FarmDetaielSerializer(farm)
        return Response(ser.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        farm=get_object_or_404(FarmModel,id=pk)
        ser=FarmDetaielSerializer(farm,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        farm=get_object_or_404(FarmModel,id=pk)
        ser=FarmDetaielSerializer(farm,data=request.data,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        farm=get_object_or_404(FarmModel,id=pk)
        farm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    




class FieldView(ModelViewSet):
    queryset=FieldModel.objects.all()
    serializer_class=FieldSerializer
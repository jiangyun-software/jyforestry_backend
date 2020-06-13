from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .predict_model import predict_cover_type
from sklearn import preprocessing
from django.views.decorators.csrf import csrf_exempt
from .models import SheetUpload,ImageUpload
from .serializers import SheetUploadSerializer,ImageUploadSerializer

#rest
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


attributes = ['Elevation', 'Aspect', 'Slope',
'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon',
'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3',
'Wilderness_Area4', 'Soil_Type1', 'Soil_Type2', 'Soil_Type3',
'Soil_Type4', 'Soil_Type5', 'Soil_Type6', 'Soil_Type7', 'Soil_Type8',
'Soil_Type9', 'Soil_Type10', 'Soil_Type11', 'Soil_Type12',
'Soil_Type13', 'Soil_Type14', 'Soil_Type15', 'Soil_Type16',
'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20',
'Soil_Type21', 'Soil_Type22', 'Soil_Type23', 'Soil_Type24',
'Soil_Type25', 'Soil_Type26', 'Soil_Type27', 'Soil_Type28',
'Soil_Type29', 'Soil_Type30', 'Soil_Type31', 'Soil_Type32',
'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40',]


def test(request):
    return HttpResponse("test")

#手动输入信息
@csrf_exempt
def form(request):
    if request.method == "POST":
        data = [[]]
        for attribute in attributes:
            data[0].append(float(request.POST[attribute]))
        data = preprocessing.StandardScaler().fit(data).transform(data)
        res = predict_cover_type(data)
        return HttpResponse(str(res))
    else:
        return HttpResponse("test")

#上传图片
class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        images = ImageUpload.objects.all()
        serializer = ImageUploadSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        images_serializer = ImageUploadSerializer(data=request.data)
        if images_serializer.is_valid():
            images_serializer.save()
            return Response(images_serializer.data)
        else:
            print('error', images_serializer.errors)
            return Response(images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SheetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        sheets = SheetUpload.objects.all()
        serializer = SheetUploadSerializer(sheets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sheets_serializer = SheetUploadSerializer(data=request.data)
        if sheets_serializer.is_valid():
            #保存到数据库
            sheets_serializer.save()
            
            #获得表格
            sheet = sheets_serializer.data["sheet"][1:]
            
   
            return Response(sheets_serializer.data)
        else:
            print('error',sheets_serializer.errors)
            return Response(sheets_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



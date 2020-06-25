from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .predict_model import predict_cover_type
from sklearn import preprocessing
from django.views.decorators.csrf import csrf_exempt
from .models import SheetUpload,ImageUpload
from .serializers import SheetUploadSerializer,ImageUploadSerializer
import os
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

#预测数据的属性
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

#返回简单的test字符串，用于测试服务器是否成功运行
@csrf_exempt
def test(request):
    return HttpResponse("test")

#接收手动输入预测信息并返回
@csrf_exempt
def form(request):
    if request.method == "POST":
        data = [[]]
        #从接收的信息中读取相应数据
        for attribute in attributes:
            data[0].append(float(request.POST[attribute]))
        #对数据进行标准化处理
        data = preprocessing.StandardScaler().fit(data).transform(data)
        #调用培训好的算法获得预测结果
        res = predict_cover_type(data)
        #返回预测结果
        return HttpResponse(str(res))
    else:
        return HttpResponse("请使用POST方式来传输信息")


#接收上传的图片，若在数据库中不存在，则将图片存入/media/upload_images/,将图片信息存入数据库
class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        images = ImageUpload.objects.all()
        serializer = ImageUploadSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        images_serializer = ImageUploadSerializer(data=request.data)
        if images_serializer.is_valid():
            #将上传的图片保存到/media/upload_images/
            images_serializer.save()
            return Response(images_serializer.data)
        else:
            print('error', images_serializer.errors)
            return Response(images_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#接收表格数据，调用培训好的算法进行预测，返回一个带有预测结果的新表格
class SheetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        sheets = SheetUpload.objects.all()
        serializer = SheetUploadSerializer(sheets, many=True)
        #获取所有上传的表格的情况
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sheets_serializer = SheetUploadSerializer(data=request.data)
        if sheets_serializer.is_valid():
            #将表格保存到/media/upload_sheets
            sheets_serializer.save()
            
            #读取接收表格中的数据
            sheet = sheets_serializer.data["sheet"][1:]#去掉路径开头的'/'
            df = pd.read_csv(sheet,engine='python')
            data = np.asarray(df[attributes])
            #数据预处理,将数据标准化
            from sklearn import preprocessing
            data = preprocessing.StandardScaler().fit(data).transform(data)
            #调用培训好的算法进行预测
            res = predict_cover_type(data)
            #给数据新增一列预测结果并导出csv文件
            df['prediction'] = res
            df.to_csv(sheet,index=False)
            #打开导出的CSV文件并返回 
            with open(sheet) as myfile:
                return HttpResponse(myfile, content_type='text/csv')
        else:
            print('error',sheets_serializer.errors)
            return Response(sheets_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



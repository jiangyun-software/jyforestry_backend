from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .predict_model import predict_cover_type
# Create your views here.
from sklearn import preprocessing
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test(request):
    if request.method == "POST":
        elevation = float(request.POST['elevation'])
        aspect = float(request.POST['aspect'])
        data = [[elevation,  aspect , -0.89,  1.65,  0.47,  1.47, -0.09,  1.32,
            0.87,  0.93,  1.79, -0.18, -0.85, -0.67, -0.16, -0.21, -0.26,
        -0.24, -0.11, -0.21,  0.  , -0.01, -0.03, -0.41, -0.17, -0.12,
        -0.18, -0.11,  0.  , -0.09, -0.21, -0.06, -0.06, -0.1 , -0.03,
        -0.15,  4.36, -0.13, -0.01, -0.06, -0.03, -0.02, -0.31, -0.22,
        -0.15, -0.22, -0.21, -0.04, -0.08, -0.03, -0.05, -0.22, -0.21,
        -0.18]]
        data = preprocessing.StandardScaler().fit(data).transform(data)
        res = predict_cover_type(data)
        return HttpResponse(str(res))
    else:
        return HttpResponse("test")
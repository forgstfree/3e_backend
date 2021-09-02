import json

from django.conf import settings
from django.core import serializers
from django.db.models import query
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path  # 用于解决中文命名文件乱码问题
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .forms import *
from .models import *

# Create your views here.

save_path = f'{settings.MEDIA_ROOT}/excel/'
save_excel_path = f'{settings.MEDIA_ROOT}/'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# @csrf_exempt
# def receiveData(request):
#     data = {}
#     data['code'] = 22222
#     data['message'] = 'The request is not valid!'
#     if request.method == 'POST':
#         tmp_file = save_path + request.FILES['file'].name
#         print(tmp_file)
#         handle_uploaded_file(tmp_file,request.FILES['file'])
#         data['code'] = 20000
#         data['message'] = 'The record is return.'
#     return JsonResponse(data)


@csrf_exempt
def createData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The file is upload fail!'
    if request.method == 'POST':
        form = UserDataFileExcelForm(
            request.POST, {'filepath': request.FILES['file']})
        if form.is_valid():
            file_model = form.save()
            real_path = save_excel_path+str(file_model.filepath)
            name_file = file_model.filename
            path_file = file_model.filepath
            type_file = name_file.split('.')[1]
            if type_file in ['xlsx','xls']:
                if type_file in ['xlsx']:
                    fileDict = pd.read_excel(real_path, sheet_name=None, engine='openpyxl')
                else:
                    fileDict = pd.read_excel(real_path, sheet_name=None)
                for name in fileDict.keys():
                    fileheader = "_|_".join(fileDict[name].columns.values.tolist())
                    headerModel = FileExcelHeader(filename=name_file, filepath=path_file, header=fileheader,filefrom=file_model, sheetname=name)
                    headerModel.save()
            elif type_file in ['csv']:
                fileDict = pd.read_csv(real_path)
                fileheader = "_|_".join(fileDict.columns.values.tolist())
                headerModel = FileExcelHeader(filename=name_file, filepath=path_file, header=fileheader,filefrom=file_model)
                headerModel.save()
            data['code'] = 20000
            data['message'] = 'The file is upload success.'
    return JsonResponse(data)


@csrf_exempt
def updateData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The file is update fail!'
    if request.method == 'POST':
        query = json.loads(request.body)
        _t = UserDataFileExcel.objects.get(pk=query['pk'])
        _t.__dict__.update(**query)
        _t.save()
        data['code'] = 20000
        data['message'] = 'The file is update success.'
    return JsonResponse(data)


@csrf_exempt
def deleteData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The file is delete fail!'
    if request.method == 'POST':
        query = json.loads(request.body)
        UserDataFileExcel.objects.get(pk=query['pk']).delete()
        data['code'] = 20000
        data['message'] = 'The file is delete success.'
    return JsonResponse(data)


@csrf_exempt
def downloadData(request):
    if request.method == 'GET':
        query = request.GET
        _t = UserDataFileExcel.objects.get(pk=query['pk'])
        filename = _t.filename
        filepath = save_excel_path + str(_t.filepath)
        file = open(filepath, 'rb')
        response =FileResponse(file)
        response['Do-Not-Intercept'] = True
        response['Access-Control-Expose-Headers']= 'Content-Disposition, Do-Not-Intercept'
        # response['Content-Disposition']='attachment;filename="models.py"'
        # response["Content-Disposition"] = "attachment; filename={0}".format(escape_uri_path(filename))
    return response


def fetchData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The list get fail!'
    if request.method == 'GET':
        data['list'] = json.loads(serializers.serialize(
            "json", UserDataFileExcel.objects.filter()))
        data['code'] = 20000
        data['message'] = 'The list get success.'
    return JsonResponse(data)

def fetchHeader(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The header list get fail!'
    if request.method == 'GET':
        data['list'] = json.loads(serializers.serialize(
            "json", FileExcelHeader.objects.filter()))
        data['code'] = 20000
        data['message'] = 'The header list get success.'
    return JsonResponse(data)


def handle_uploaded_file(p, f):
    with open(p, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

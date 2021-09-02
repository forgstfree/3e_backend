import json

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mathmodel.ipat import MathModel_PAT

from .forms import *
from .models import UserMathModel

# Create your views here.

save_excel_path = f'{settings.MEDIA_ROOT}/'

@csrf_exempt
def createData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The model is create fails!'
    if request.method == 'POST':
        query = json.loads(request.body)
        form = PickForm(query)
        if form.is_valid():
            mathmodel = form.save(commit=False)
            mathmodel.desc = query['desc']
            mathmodel.remake = query['remake']
            mathmodel.save()
            data['code'] = 20000
            data['message'] = 'The model is create success'
        else:
            data['message'] = form.errors
    return JsonResponse(data)

@csrf_exempt
def deleteData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The model is delete fail!'
    if request.method == 'POST':
        query = json.loads(request.body)
        UserMathModel.objects.get(pk=query['pk']).delete()
        data['code'] = 20000
        data['message'] = 'The model is delete success.'
    return JsonResponse(data)

def fetchData(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The list get fails!'
    if request.method == 'GET':
        data['list'] = json.loads(serializers.serialize(
            "json", UserMathModel.objects.filter()))
        data['code'] = 20000
        data['message'] = 'The list get success.'
    return JsonResponse(data)

@csrf_exempt
def createAnalysis(request):
    data = {}
    data['code'] = 22222
    data['message'] = 'The analysis is fails!'
    if request.method == 'POST':
        query = json.loads(request.body)
        print(query)
        if query['pk'] != "":
            m_pat = MathModel_PAT()
            r = m_pat.counter(save_excel_path,query['coefficient'],query['variable'])
            print(r)
            data['result'] = "_|_".join(r.astype(str))
            data['code'] = 20000
            data['message'] = 'The analysis success'
    return JsonResponse(data)

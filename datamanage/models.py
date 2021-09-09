from django.db import models

# Create your models here.

# class WorkBook(models.Model):
#     name = models.CharField(max_length=400)
#     # 通过字典结构将sheet的真名与uuid对应起来
#     sheets = models.TextField()

# class List(models.Model):
#     uoloader = models.CharField(max_length=200)
#     upload_date = models.DateTimeField('date uploaded', auto_now_add=True, null=True)
#     name = models.CharField(max_length=400)
#     # id_name = models.CharField(max_length=100)
#     id_name = models.OneToOneField('WorkBook', on_delete=models.CASCADE)

class UserDataFileExcel(models.Model):
    filename = models.CharField(max_length=400)
    filepath = models.FileField(upload_to='excel/')
    uploader = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True, null=True)
    tag = models.CharField(max_length=400)

class FileExcelHeader(models.Model):
    filename = models.CharField(max_length=400)
    filepath = models.CharField(max_length=600)
    header = models.TextField()
    sheetname = models.CharField(max_length=400)
    filefrom = models.ForeignKey('UserDataFileExcel', on_delete=models.CASCADE)


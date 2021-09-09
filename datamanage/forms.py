from django.forms import ModelForm
from .models import *


class UserDataFileExcelForm(ModelForm):
    class Meta:
        model = UserDataFileExcel
        fields = ['filename', 'uploader', 'filepath', 'tag']
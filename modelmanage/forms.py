from django.forms import ModelForm
from .models import UserMathModel

class PickForm(ModelForm):
  class Meta:
    model = UserMathModel
    fields = ['name','expression','coefficient','variable']
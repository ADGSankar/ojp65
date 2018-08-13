from django import forms
from ojp.models import *

type_list = [('none','None'),('schooling','Schooling'),('inter', 'Inter'), ('diploma', 'Diploma'),('degree','Degree'),('btech','Btech'),('mtech','Mtech'),('mba','MBA'),('mca','MCA'),('others','Others')]
class JobSeekerDetails(forms.Form):
    dp=forms.ImageField(required=True)
    resume=forms.FileField(required=False)
    email=forms.EmailField(max_length=40,required=True)
    mobile=forms.CharField(max_length=10,required=True)
    o_details= forms.CharField(widget=forms.Textarea)

class JobSeekerStudyDetails(forms.Form):
    type=forms.CharField(widget=forms.Select(choices=type_list))
    clz_name = forms.CharField(max_length=50, required=True)
    specilization=forms.CharField(max_length=50, required=True)
    pyear = forms.IntegerField(required=True)
    percentage = forms.FloatField(required=True)

class JobSeekerExperianceDetails(forms.Form):
    c_name=forms.CharField(max_length=20, required=True)
    designation=forms.CharField(max_length=20, required=True)
    experiance=forms.FloatField()





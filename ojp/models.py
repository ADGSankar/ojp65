from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CUser(AbstractUser):
     is_jp = models.BooleanField(default=False)

class JSDetails(models.Model):
    dp = models.FileField(default=None)
    resume = models.FileField(default=None, )
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    o_details= models.TextField(max_length=100)
    js = models.OneToOneField(CUser, on_delete=models.CASCADE,default=None)

class JSSDetails(models.Model):
    type = models.CharField(max_length=10)
    clz_name = models.CharField(max_length=50)
    specilization = models.CharField(max_length=50)
    pyear = models.IntegerField()
    percentage = models.FloatField()
    js=models.ForeignKey(CUser,on_delete=models.CASCADE)

class JSEDetails(models.Model):
    c_name=models.CharField(max_length=20)
    designation=models.CharField(max_length=20)
    experiance=models.FloatField()
    js = models.ForeignKey(CUser, on_delete=models.CASCADE)

class JPDetails(models.Model):
    jp=models.ForeignKey(CUser,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=50)
    dp=models.FileField()
    admin_name=models.CharField(max_length=30)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)


class JPPostJobs(models.Model):
    jp=models.ForeignKey(CUser,on_delete=models.CASCADE)
    cdetails=models.ForeignKey(JPDetails,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=50)
    salary=models.FloatField()
    work_hours=models.IntegerField()
    required_experiance=models.IntegerField()
    qualifications=models.TextField(max_length=100)
    note=models.TextField(max_length=100)



class JSAppliedJobs(models.Model):
    job = models.ForeignKey(JPPostJobs, on_delete=models.CASCADE)
    js = models.ForeignKey(CUser, on_delete=models.CASCADE)
    is_selected=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    reason=models.TextField(max_length=100,default="")
    notes=models.TextField(max_length=100,default="")
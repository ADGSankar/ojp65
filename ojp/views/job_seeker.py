from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView,TemplateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate,logout,login
from ojp.models import *
from ojp.templates.forms.login import *
from ojp.templates.forms.jobseekerdetails import *
from ojp.templates.forms.jobproviderdetails import *
import sys
from django.db.utils import IntegrityError
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import FormMessagesMixin
import os


def handle_uploaded_file(path):
    os.unlink(path)




class JSLoginController(View):
    def get(self,request):
        # import ipdb
        # ipdb.set_trace()
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            form=Login()
            return render(request,
                template_name="jslogin.html",
                context={'form' :form}
            )
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        # import ipdb
        # ipdb.set_trace()
        if user is not None and user.is_jp is False:
            login(request, user)
            # messages.add_message(self.request,messages.SUCCESS,'Login Successful')
            return redirect("ojp:jshome")
        else:
            messages.error(self.request,"Invalid username / password")
            return redirect("ojp:jslogin")

class JSSignupController(View):
    def get(self,request):
        form=SignUp()
        return render(request,
            template_name="jssignup.html",
            context={'form' :form}
        )
    def post(self, request, *args, **kwargs):
            # import ipdb
            # ipdb.set_trace()
            try:
                i = CUser.objects.create_user(username=request.POST['username'], password=request.POST['password'],first_name=request.POST['first_name'], last_name=request.POST['last_name'],is_jp=False)
            except  IntegrityError:
                messages.error(request,message="Username already exists.Please choose another username")
                return redirect('ojp:jssignup')

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('ojp:jsdetails')



def JSLogoutControl(request):
    logout(request)
    return redirect("ojp:home")



class JobSeekersHome(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JSDetails.objects.filter(js=request.user)
            return render(request,
                template_name=r"web/js/jshome.html",
                context={'req':request,'jsd':jsd[0]}
            )


class JobSeekersHelpDesk(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JSDetails.objects.filter(js=request.user)
            return render(request,
                template_name=r"web/js/jshd.html",
                context={'req':request,'jsd':jsd[0]}
            )

class JobSeekersResume(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JSDetails.objects.filter(js=request.user)
            return render(request,
                template_name=r"web/js/jsresume.html",
                context={'req':request,'jsd':jsd[0]}
            )


class JobSeekersProfile(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            form=JobSeekerDetails
            jsd=JSDetails.objects.filter(js=request.user)
            jssd=JSSDetails.objects.filter(js=request.user)
            jsed=JSEDetails.objects.filter(js=request.user)
            return render(request,
                template_name=r"web/js/jsprofile.html",
                context={'form':form,'jsd':jsd[0],'jssd':jssd,'jsed':jsed}
            )

    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        jsd = JSDetails.objects.get(js=request.user)
        old_dp = jsd.dp
        new_dp = request.FILES.get("dp")
        old_res=jsd.resume
        new_res=request.FILES.get("resume")
        if new_dp != None:
            new_dp.name = (new_dp.name).lower()
            if (new_dp.name).endswith(".jpg") or (new_dp.name).endswith(".jpeg") or (new_dp.name).endswith(".png"):
                handle_uploaded_file("ojp/media/" + old_dp.name)
                jsd.dp = request.FILES.get('dp', None)

        if new_res != None:
            new_res.name = (new_res.name).lower()
            if (new_res.name).endswith(".pdf") or (new_res.name).endswith(".docx") :
                handle_uploaded_file("ojp/media/" + old_res.name)
                jsd.resume = request.FILES.get('resume')

        jsd.email = request.POST["email"]
        jsd.mobile = request.POST["mobile"]
        jsd.o_details=request.POST["o_details"]
        jsd.save()

        return redirect("ojp:jsprofile")

class JobSeekersViewJobs(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JSDetails.objects.filter(js=request.user)
            vj=JPPostJobs.objects.all()
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsvj.html",
                context={'jobs':vj,'req':request,'jsd':jsd[0]}
            )

def AppliedJobDelete(request,pk):
    # import ipdb
    # ipdb.set_trace()
    JSAppliedJobs.objects.filter(job=pk,js=request.user.id).delete()
    return redirect("ojp:jsvaj")

def JobSeekerApplyJob(request,pk):
    jsa = JSAppliedJobs.objects.filter(job=pk,js=request.user.id)
    # import ipdb
    # ipdb.set_trace()
    if not jsa:
        jsa=JSAppliedJobs()
        jsa.job=JPPostJobs.objects.filter(id=pk)[0]
        jsa.js=request.user
        jsa.save()
        return redirect("ojp:jsvj")
    else:
        return render(request, r"web/js/notification_page.html",context={"req":request})
class JobSeekerViewJob(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JSDetails.objects.filter(js=request.user)
            aj=JPPostJobs.objects.filter(id=pk)
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsaj.html",
                context={'aj':aj[0],'req':request,'jsd':jsd[0]}
            )

class JobSeekersAppliedJobs(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JSDetails.objects.filter(js=request.user)
            vaj=JSAppliedJobs.objects.filter(js=request.user.id)

            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsvaj.html",
                context={'jobs':vaj,'req':request,'jsd':jsd[0]}
            )

class AppliedJobStatus(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JSDetails.objects.filter(js=request.user)
            aj=JSAppliedJobs.objects.filter(job=pk,js=request.user.id)
            if aj:

                if aj[0].is_selected:
                    return render(request, r"web/js/jsastatus.html",context={"req":request,"aj":aj[0],'jsd':jsd[0]})
                elif aj[0].is_rejected:
                    return render(request, r"web/js/jsrstatus.html",context={"req":request,"aj":aj[0],'jsd':jsd[0]})
            return render(request, r"web/js/jsnostatus.html", context={"req": request,'jsd':jsd[0]})


class JobSeekersDetails(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        form = JobSeekerDetails
        jssd=JSSDetails.objects.filter(js=request.user)
        jsed=JSEDetails.objects.filter(js=request.user)
        return render(request,
            template_name=r"web/js/jsdetails.html",
            context={'form': form,'jssd':jssd,'jsed':jsed}
        )
    def post(self, request, *args, **kwargs):
        jsd=JSDetails()
        # import ipdb
        # ipdb.set_trace()
        jsd.dp=request.FILES.get('dp',None)
        jsd.resume=request.FILES.get('resume',None)
        jsd.email=request.POST["email"]
        jsd.mobile=request.POST["mobile"]
        jsd.o_details=request.POST["o_details"]
        jsd.js=request.user
        jsd.save()
        logout(request)
        return redirect('ojp:jslogin')

class JobSeekersStudyDetails(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        form=JobSeekerStudyDetails
        return render(request,
                      template_name=r"web/js/jssd.html",
                      context={'form':form})

    def post(self, request, *args, **kwargs):
        jssd=JSSDetails()
        jssd.type=request.POST["type"]
        jssd.clz_name=request.POST["clz_name"]
        jssd.specilization=request.POST["specilization"]
        jssd.pyear=request.POST["pyear"]
        jssd.percentage=request.POST["percentage"]
        jssd.js=request.user
        jssd.save()
        return redirect('ojp:jsprofile')

class JobSeekersStudyDetailsEdit(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request,pk):
        jssd=JSSDetails.objects.get(id=pk)
        return render(request,
                      template_name=r"web/js/jssdedit.html",
                      context={'jssd': jssd})

    def post(self,request,*args,**kwargs):
        jssd=JSSDetails.objects.get(id=kwargs['pk'])
        jssd.type = request.POST["type"]
        jssd.clz_name = request.POST["clz_name"]
        jssd.specilization = request.POST["specilization"]
        jssd.pyear = request.POST["pyear"]
        jssd.percentage = request.POST["percentage"]
        jssd.save()
        return redirect('ojp:jsprofile')

def JobSeekersStudyDetailsDelete(request,pk):
    JSSDetails.objects.filter(id=pk).delete()
    return redirect("ojp:jsprofile")

class JobSeekersExperianceDetails(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        form=JobSeekerExperianceDetails
        return render(request,
                      template_name=r"web/js/jsed.html",
                      context={'form':form})

    def post(self, request, *args, **kwargs):
        jsed=JSEDetails()
        jsed.c_name=request.POST["c_name"]
        jsed.designation=request.POST["designation"]
        jsed.experiance= request.POST["experiance"]
        jsed.js=request.user
        jsed.save()
        return redirect('ojp:jsprofile')

class JobSeekersExperianceDetailsEdit(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request,pk):
        jsed=JSEDetails.objects.get(id=pk)
        return render(request,
                      template_name=r"web/js/jsededit.html",
                      context={'jsed': jsed})
    def post(self, request, *args, **kwargs):
        jsed=JSEDetails.objects.get(id=kwargs['pk'])
        jsed.c_name=request.POST["c_name"]
        jsed.designation=request.POST["designation"]
        jsed.experiance= request.POST["experiance"]
        jsed.js=request.user
        jsed.save()
        return redirect('ojp:jsprofile')

def JobSeekersExperianceDetailsDelete(request,pk):
    JSEDetails.objects.filter(id=pk).delete()
    return redirect("ojp:jsprofile")

class JobSeekerledit(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            ud=CUser.objects.filter(id=request.user.id)
            jsd = JSDetails.objects.filter(js=request.user)
            # form=JobProviderDetails1()
            return render(request,
                template_name=r"web/js/jsledit.html",
                context={'ud':ud[0],'jsd':jsd[0]}
            )

    def post(self, request, *args, **kwargs):
        ud=CUser.objects.get(username=request.user.username)
        ud.first_name=request.POST["first_name"]
        ud.last_name=request.POST["last_name"]
        ud.username=request.POST["username"]
        if request.POST["password"] != '':
            ud.set_password(request.POST["password"])
        try:
            ud.save()
        except IntegrityError:
            messages.error(request, message="Username already exists.Please choose another username")
            return redirect('ojp:jsledit')

        return redirect("ojp:jsprofile")


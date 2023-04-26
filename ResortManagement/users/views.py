from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
# Create your views here.

def indexView(request):
    return render(request,"users/index.html")

def userHomeView(request):
    return render(request,"users/home.html",locals())

@staff_member_required
def staffHomeView(request):
    return render(request,"users/staffHome.html")

def userRegisterView(request):
    cache.clear()
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        user=CustomUser.objects.filter(email=request.POST['email']).first()
        print(user)
        if not user: 
            if form.is_valid():
                my_user=CustomUser.objects.create_user(email=request.POST['email'],
                                                    password=request.POST['password'],
                                                    first_name=request.POST['first_name'],
                                                    last_name=request.POST['last_name'],
                                                    gender=request.POST['gender'],
                                                    age=request.POST['age'],
                                                    flat_no=request.POST['flat_no'],
                                                    area=request.POST['area'],
                                                    city=request.POST['city'],
                                                    state=request.POST['state'],
                                                    pincode=request.POST['pincode'])
                return redirect("login")
        else:
            messages.error(request,"Email already exists")
    else:
        form=CustomUserCreationForm
        # return render(request,"users/register.html",{"form":form})
    form=CustomUserCreationForm
    return render(request,"users/register.html",{"form":form})

def loginView(request):
    if request.method=="POST":
        print(request)
        email=request.POST['email']
        password=request.POST['password']
        if email is None or password is None:
            messages.error(request,"Check with your credentials")
        else:
            my_user=authenticate(request,email=email,password=password)
            if my_user is not None:
                login(request,my_user)
                
                if my_user.is_staff:
                    return redirect('staffhome')
                else:
                    return redirect('userhome')
            else:
                # return HttpResponse("User not found")
                messages.error(request,"User Not found")
    else:
        form=UserLoginForm()
        return render(request,"users/login.html",{'form':form})
    form=UserLoginForm
    return render(request,"users/login.html",{'form':form})

def logoutView(request):
    logout(request)
    return redirect('index')


class StaffCreationView(FormView):
    form_class=CustomStaffCreationForm
    success_url=reverse_lazy("login")
    template_name="users/empreg.html"

    def post(self,request,*args,**kwargs):
        print(request.POST)
        return super().post(request,*args,**kwargs)
        # return super().post(request,*args,**kwargs)
    def form_valid(self,form):
        # form=self.form_class(data=form.data)
        user=CustomUser.objects.filter(email=form.data['email']).first()
        if not user: 
            form.save()
            # my_user=CustomUser.objects.create_staff(email=form.data['email'],
            #                                         password=form.data['password'],
            #                                         first_name=form.data['first_name'],
            #                                         last_name=form.data['last_name'],
            #                                         gender=form.data['gender'],
            #                                         age=form.data['age'],
            #                                         flat_no=form.data['flat_no'],
            #                                         area=form.data['area'],
            #                                         city=form.data['city'],
            #                                         state=form.data['state'],
            #                                         pincode=form.data['pincode'])
            # form=CustomStaffCreationForm
            # return super().form_valid(form)
            
        else:
            messages.error(self.request,"Check with your data")
            # print("no")
            # return messages.error(super().request,message="no user")
            # print("testing")
            # form=CustomStaffCreationForm
            # return render(super().request,"users/empreg.html",{'form':form})
        return super().form_valid(form)
        # return super().post(form.data)

    def form_invalid(self, form):
        messages.error(self.request,"User Already exists")
        # return redirect('staffregister')
        # return HttpResponse("User Already exists")
        return super().form_invalid(form)


        


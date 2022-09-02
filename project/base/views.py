from ntpath import join
import re
from django.shortcuts import render,redirect
from .models import Group,Report,User
from .forms import GroupForm, ReportForm
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm,UserRegisterFormAdmin




# Create your views here.

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User is not existed!!!!')
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request,user)
            return redirect("main_page")
        else:
            messages.error(request, 'Wrong username or password')

    context = {}
    return render(request, 'base/login-form.html',context)


def logout_user(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url='login_page')
def main_page(request):
    groups = Group.objects.all()
    reports = Report.objects.all()
    users = User.objects.all()
    context = {'title':'Main', 'number_of_groups':len(groups), 'number_of_reports':len(reports), 'number_of_users':users.count()}
    return render(request, 'base/main.html' , context)


@login_required(login_url='login_page')
def group_page(request):
    groups = Group.objects.all()
    user_is = request.user.id
    group_is = Group.objects.filter(user__id = user_is)
    context = {'title':'Group Management', 'groups':groups , 'group_is':group_is}
    return render(request,'base/group.html',context)



@login_required(login_url='login_page')
def create_group_page(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("group_page")
    context = {'form':form}
    return render(request,'base/create-groupe.html',context)

@login_required(login_url='login_page')
def update_group_page(request,pk):
    group_is = Group.objects.get(id = pk)
    form = GroupForm(instance=group_is)
    if request.method == "POST":
        form = GroupForm(request.POST,instance=group_is)
        if form.is_valid():
            form.save()
            return redirect("group_page")
    context = {'form':form}
    return render(request,'base/create-groupe.html',context)


@login_required(login_url='login_page')
def view_group_page(request,pk):
    group_is = Group.objects.get(id = pk)
    print(group_is.update.date())
    user_number = len(group_is.user_set.all())
    user_report = len(group_is.report_set.all())
    
    context = {'group_is':group_is, 'user_number':user_number , 'user_report':user_report}
    return render(request,'base/view-groupe.html',context)


@login_required(login_url='login_page')
def delete_group_page(request,pk):
    group_is = Group.objects.get(id = pk)
    if request.method == "POST":
        group_is.delete()
        return redirect("group_page")
    context = {'group_is':group_is}
    return render(request,'base/delete-group.html',context)

@login_required(login_url='login_page')
def report_page(request):
    reports = Report.objects.all()

    user_is = request.user.id
    report_is = Report.objects.filter(user__id = user_is)
    
   
    context = {'reports':reports , 'report_is':report_is}
    return render(request,'base/report.html',context)

@login_required(login_url='login_page')
def create_report_page(request):
    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("report_page")
    context = {'form':form}
    return render(request,'base/create-report.html',context)

@login_required(login_url='login_page')
def update_report_page(request,pk):
    report_is = Report.objects.get(id = pk)
    form = ReportForm(instance=report_is)
    if request.method == "POST":
        form = ReportForm(request.POST,request.FILES,instance=report_is)
        if form.is_valid():
            form.save()
            return redirect("report_page")
    context = {'form':form}
    return render(request,'base/create-report.html',context)

@login_required(login_url='login_page')
def delete_report_page(request,pk):
    report_is = Report.objects.get(id = pk)
    if request.method == "POST":
        report_is.delete()
        return redirect("report_page")
    context = {'report_is':report_is}
    return render(request,'base/delete-report.html',context)


@login_required(login_url='login_page')
def view_report_page(request,pk):
    report_is = Report.objects.get(id = pk)
    print(report_is.upload_file.url)
    context = {'report_is':report_is}
    return render(request,'base/view-report.html',context)



@login_required(login_url='login_page')
def usermanagment_page(request):
    users = User.objects.all()
    user_group = dict()
    
    for user in users:
        group = Group.objects.filter(user__id = user.id)
        if group:
            user_group[user] = group
        else:
            user_group[user] = 'No Group'
    
    context = {'user_group':user_group}
    return render(request, 'base/usermanagment.html',context)

@login_required(login_url='login_page')
def create_usermanagment_page(request):

    # form = UserRegisterForm()
    # if request.method == "POST":
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form.save_m2m()
    #         return redirect("role_page")
    # context = {'form':form}

    if request.user.is_superuser:
        formAdmin = UserRegisterFormAdmin()
    else:
        formUser = UserRegisterForm()

    if request.method == "POST":
        if request.user.is_superuser:
            formAdmin = UserRegisterFormAdmin(request.POST)
            if formAdmin.is_valid():
                formAdmin.save()
                formAdmin.save_m2m()
                return redirect("role_page")
        else:
            formUser = UserRegisterForm(request.POST,)
            if formUser.is_valid():
                formUser.save()
                formUser.save_m2m()
                return redirect("role_page")

    if request.user.is_superuser:
        form = formAdmin
    else:
        form = formUser
    context = {'form':form}
    return render(request, 'base/create-usermanagment.html',context)



@login_required(login_url='login_page')
def update_usermanagment_page(request,pk):
    user_is = User.objects.get(id = pk)
    
    if request.user.is_superuser:
        formAdmin = UserRegisterFormAdmin(instance=user_is)
    else:
        formUser = UserRegisterForm(instance=user_is)

    if request.method == "POST":
        if request.user.is_superuser:
            formAdmin = UserRegisterFormAdmin(request.POST,instance=user_is)
            if formAdmin.is_valid():
                formAdmin.save()
                formAdmin.save_m2m()
                return redirect("role_page")
        else:
            formUser = UserRegisterForm(request.POST,instance=user_is)
            if formUser.is_valid():
                formUser.save()
                formUser.save_m2m()
                return redirect("role_page")

    if request.user.is_superuser:
        form = formAdmin
    else:
        form = formUser
    context = {'form':form}
    return render(request,'base/create-usermanagment.html',context)

@login_required(login_url='login_page')
def delete_usermanagment_page(request,pk):
    user_is = User.objects.get(id = pk)
    if request.method == "POST":
        user_is.delete()
        return redirect("usermanagment_page")
    context = {'user_is':user_is}
    return render(request,'base/delete-user.html',context)

@login_required(login_url='login_page')
def view_user_page(request,pk):
    user_is = User.objects.get(id = pk)
    report_number = len(user_is.report_set.all())
    group_list = []
    group_name = ""
    group = Group.objects.filter(user__id = pk)
    if group:
        for gr in group:
            group_list.append(gr.name)
        group_name = "-".join(group_list)
    else:
        group_name = "No Group"

    context = {'user_is':user_is, 'report_number':report_number , 'group_name':group_name}
    return render(request,'base/view-user.html',context)



@login_required(login_url='login_page')
def role_page(request):
    users = User.objects.all()
    user_group = dict()
    
    for user in users:
        group = Group.objects.filter(user__id = user.id)
        if group:
            user_group[user] = group
        else:
            user_group[user] = 'No Group'
    print(user_group)
    
    context = {'user_group':user_group}
    return render(request, 'base/role.html',context)
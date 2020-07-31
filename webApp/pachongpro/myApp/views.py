from django.shortcuts import render

# Create your views here.

def info(request):
    from .xp_modules import getPositionSalaryDic
    salaryDic = getPositionSalaryDic()
    return render(request, "info.html", {'num': salaryDic["num"]})


def index(request):
    return render(request, "index.html")




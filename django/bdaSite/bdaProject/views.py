from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {}
    return render(request, 'bdaProject/index.html', context)

def org(request, org):
    
    context = {
        'org_name' : org
    }
    return render(request, 'bdaProject/organization.html', context)

from django.http import response
from django.shortcuts import redirect, render
from .models import Contact
# Create your views here.


def index(request):
    qId = request.POST['qId']
    url = "https://codeforces.com/problemset/problem/"
    for c in qId:
        if c != ' ':
            url = url + c
        else:
            url = url + '/'
    response = redirect(url)
    return response


def contact(request):
    return render(request, 'contact.html')


def success(request):
    if request.method == "POST":
        print(":)\n")
        name = request.POST['name']
        email = request.POST['email']
        suggestion = request.POST['suggestion']
        ins = Contact(name=name, email=email, suggestion=suggestion)
        ins.save()

    return render(request, 'success.html')

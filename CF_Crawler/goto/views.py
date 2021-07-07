from django.http import response
from django.shortcuts import redirect, render

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

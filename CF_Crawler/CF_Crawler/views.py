from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

# html = """<!DOCTYPE html ><html lang = "en" >   <head >        <meta charset = "UTF-8" / >        <meta http-equiv = "X-UA-Compatible" content = "IE = edge" / >        <meta name = "viewport" content = "width = device-width, initial-scale = 1.0" / >        <title > Document < /title >    </head >    <body >        <form action = "/stats" method="post" id="form1">            <label for = "handle">CF Handle:</label>            <input type = "text" id="handle" name="handle" /><br />        </form >        <button type = "submit" form="form1" value="Submit">Submit</button>    </body ></html >"""


# def index(request):
#     return HttpResponse("index.html")

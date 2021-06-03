from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

# html = """<!DOCTYPE html ><html lang = "en" >   <head >        <meta charset = "UTF-8" / >        <meta http-equiv = "X-UA-Compatible" content = "IE = edge" / >        <meta name = "viewport" content = "width = device-width, initial-scale = 1.0" / >        <title > Document < /title >    </head >    <body >        <form action = "/stats" method="post" id="form1">            <label for = "handle">CF Handle:</label>            <input type = "text" id="handle" name="handle" /><br />        </form >        <button type = "submit" form="form1" value="Submit">Submit</button>    </body ></html >"""


# def index(request):
#     return HttpResponse("index.html")


<div class = "container mx-3 my-3" >
      <form method = "post" >
        <div class = "mb-3" >
          <label for = "CF Handle" class = "form-label" > Handle < /label >
          <input type = "text" class = "form-control" id = "handle" aria-describedby = "emailHelp" >
          <div id = "handle" class = "form-text" > We'll never share your handle with anyone else. < /div >
        </div >
        <button type = "submit" class = "btn btn-primary" > Submit < /button >
      </form >
    </div>

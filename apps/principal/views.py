import os, shutil
from django.conf import settings
from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
# Create your views here.

def inicio(request):
	
	return render( request, "inicio.html")

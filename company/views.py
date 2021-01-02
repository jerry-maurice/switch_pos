from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User

import logging, json
from datetime import date, datetime
from django.utils import timezone

from fund.models import Fund, Transaction
from account.models import Account
from company.models import Company

# get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def order_submission(request):
    received_json = json.loads(request.body)
    logger.info(received_json)
    return render(request, 'register/register.html')
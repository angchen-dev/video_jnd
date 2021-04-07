from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone


from videoJnd.src.ProcessRequest import process_request

# home page
def home(request):
    return render(request,'index.html')

def etjnd(request):
    return render(request,'et_index.html')


@csrf_exempt
def scheduler(request):
    return JsonResponse(process_request(request), safe=False)
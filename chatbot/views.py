from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from random import randint

from chatbot.models import Jokes
# Create your views here.
def home(request):
    return render(request,'chatbot/index.html')

@csrf_exempt
def message(request):
    if request.method == "POST":
        body = request.read().decode("utf-8") 
        body = json.loads(body)
        message = body['message'].lower()
        reqType = body['reqType']

        print(reqType)

        if(reqType == 'store_joke'):
            newJoke=Jokes.objects.create(joke=message)
            newJoke.save()
            resp={
                'message':'Thank you for telling me a Joke!',
                'resType':'done'
            }
        elif(reqType == 'name'):
            resp={
                'message': message + ', who?',
                'resType':'ask_joke'
            }
        elif("knock knock" in message):
            resp={
                'message':'who is there?',
                'resType':'ask_name'
            }
        elif("tell me a joke" in message):
            jokes = Jokes.objects.all()
            size = jokes.count()
            print(size)
            if(size==0):
                resp={
                    'message':'I do not have any joke. Please tell me a joke',
                    'resType':'none'
                }
            else:
                resJoke = Jokes.objects.order_by('?')[0].joke
                print(resJoke)
                resp={
                    'message':resJoke,
                    'resType':'none'
                }
        elif(reqType == 'none'):
            resp={
                    'message':'Sorry, I did not get you!',
                    'resType':'none'
                }
        return JsonResponse(resp)
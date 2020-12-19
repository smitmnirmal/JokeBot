from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from random import randint
from chatbot.models import Jokes

#home page
def home(request):
    return render(request,'chatbot/index.html')

#disabling csrf requirement
@csrf_exempt
def message(request):
    #handling post request
    if request.method == "POST":
        body = request.read().decode("utf-8") 
        body = json.loads(body)
        message = body['message'].lower()
        reqType = body['reqType']

        # store joke to db
        if(reqType == 'store_joke'):
            name = request.session.get('set_joke_name')
            newJoke=Jokes.objects.create(joke=message, person_name=name)
            newJoke.save()
            resp={
                'message':'Thank you for telling me a Joke!',
                'resType':'done'
            }
        # responding to user's greeting message
        elif("hi" in message or "hello" in message or "hey" in message):
            resp={
                'message':'Hello, how can I help you?',
                'resType':'done'
            }
        # responding to user's laugh
        elif("haha" in message or "ha ha" in message):
            resp={
                'message':':)',
                'resType':'done'
            }
        # storing name for joke 
        elif(reqType == 'name'):
            request.session['set_joke_name'] = message
            resp={
                'message': message + ', who?',
                'resType':'ask_joke'
            }
        # getting joke and sending it back to user
        elif(reqType == 'get_person_joke' and "who" in message):
            joke_person = request.session.get('get_joke')
            resp={
                'message': joke_person,
                'resType':'done'
            }
        # responding to user's knock knock
        elif("knock knock" in message):
            resp={
                'message':'who is there?',
                'resType':'ask_name'
            }
        # sending name from joke
        elif("who is there" in message or "who's there" in message):
            person_name = request.session.get('get_joke_name')
            
            resp={
                'message':person_name,
                'resType':'get_joke'
            }
        # getting random joke from db and storing it inside session for global accessibility
        elif("tell me a joke" in message):
            jokes = Jokes.objects.all()
            size = jokes.count()
            if(size==0):
                resp={
                    'message':'I do not have any joke. Please tell me a joke',
                    'resType':'none'
                }
            else:
                newJoke = Jokes.objects.order_by('?')[0]
                request.session['get_joke_name'] = newJoke.person_name
                request.session['get_joke'] = newJoke.joke

                resp={
                    'message':'knock knock',
                    'resType':'none'
                }
        #responding to reqType none
        elif(reqType == 'none'):
            resp={
                    'message':'Sorry, I did not get you!',
                    'resType':'none'
                }
        #handling unwanted error
        else:
            resp={
                    'message':'Something went wrong! Please try again',
                    'resType':'none'
                }
        return JsonResponse(resp)
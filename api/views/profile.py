import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import CustomUser, Article, Category, Comment
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

@csrf_exempt
@login_required
def profile(request: HttpRequest) -> JsonResponse:
    #perform the following only if the request is a GET request
    if request.method == 'GET':
        #get the user object from the request
        user = request.user
        #return a JsonResponse with the following data
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            #'profile_image': user.profile_image,
            'categories': [category.name for category in user.categories.all()],
        })
    #modify the user profile if the request method is a PUT request
    elif request.method == 'PUT':
        try:
            #get the user object from the request
            user = request.user
            print(user)
            data = request.body
            # decode the binary data to string
            data_str = data.decode('utf-8')
            # convert the string data to a dictionary
            data_dict = json.loads(data_str)
            print(data_dict)
            #update the user object with the data
            user.username = data_dict['username'] if 'username' in data_dict else user.username
            user.email = data_dict['email'] if 'email' in data_dict else user.email
            user.date_of_birth = data_dict['date_of_birth'] if 'date_of_birth' in data_dict else user.date_of_birth
            #user.profile_image = data_dict['profile_image'] if 'profile_image' in data_dict else user.profile_image
            #save the user object
            user.save()
            print(user)
            #return a status 200 response
            return HttpResponse(status=200)
        except Exception as e:
            #return a status 400 response
            return HttpResponse(status=400, reason=e)
    #delete the user object if the request method is a DELETE request
    elif request.method == 'DELETE':
        try:
            #get the user object from the request
            user = request.user
            #delete the user object
            user.delete()
            #return a status 200 response
            return HttpResponse(status=200)
        except Exception as e:
            #return a status 400 response
            return HttpResponse(status=400, reason=e)
    #create a new user object if the request method is a POST request
    elif request.method == 'POST':
        try:
            #get the data from the request body
            data = request.body
            #decode the binary data to string
            data_str = data.decode('utf-8')
            #convert the string data to a dictionary
            data = json.loads(data_str)

            User = get_user_model()

            #create a new user object with the data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                date_of_birth=data['date_of_birth'],
                #profile_image=data['profile_image'],
                password=data['password'],
            )
            #return a status 201 response (new resourse created)
            return HttpResponse(status=201)
        except Exception as e:
            #return a status 400 response
            return HttpResponse(status=400, reason=e)
    # else return an error
    else:
        #return a status 405 response (method not allowed)
        return HttpResponse(status=405)

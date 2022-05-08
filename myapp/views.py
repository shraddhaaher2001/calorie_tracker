from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    elif request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("/")
        else:
            # Return an 'invalid login' error message.
            return render(request,"login.html")
    return render(request,"login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")

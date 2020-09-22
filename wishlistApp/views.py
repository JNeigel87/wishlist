from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "registration.html")

def register(request):
    print(request.POST)
    validatedErrors = User.objects.baseValidator(request.POST)
    if len(validatedErrors)>0:
        for key, value in validatedErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        newMem = User.objects.create(
        name = request.POST["name"],
        username = request.POST["username"],
        password = request.POST["password"]
        )

        request.session['logId'] = newMem.id
        return redirect("/success")

def login(request):
    print(request.POST)
    resultedFilter = User.objects.filter(username = request.POST['username'])
    validatedErrors = User.objects.loginValidation(request.POST)
    if len(validatedErrors)>0:
        for key, value in validatedErrors.items():
            messages.error(request, value)
        return redirect("/")
    request.session['logId'] = resultedFilter[0].id
    return redirect("/homepage")

def success(request): 
    newMem = User.objects.get(id = request.session['logId'])

    context = {
        'newMem': newMem
    }

    return render(request, "main.html", context)

def homepage(request):
    if 'logId' not in request.session:
        return redirect("/")
    member = User.objects.get(id = request.session['logId'])
    
    context = {
        "member": member,
        "item": Item.objects.all(),
        "addedBy": Item.objects.filter(addedBy= User.objects.get(id=request.session['logId'])),
        "favedItems": Item.objects.filter(favoritedby= User.objects.get(id=request.session['logId'])),
        "listedBy": Item.objects.exclude(addedBy= User.objects.get(id=request.session['logId'])),
        "unfavedItems": Item.objects.exclude(favoritedby= User.objects.get(id=request.session['logId'])),
    }
    return render(request, "home.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def newitem(request):
    
    return render(request, "newItem.html")

def createItem(request):
    validatedErrors = Item.objects.itemvalidation(request.POST)
    if len(validatedErrors)>0:
        for key, value in validatedErrors.items():
            messages.error(request, value)
        return redirect("/newitem")
    # items= Item.objects.create(
    #     itemname = request.POST["itemname"],
    #     addedby = User.objects.get(id = request.session['username'])
    # )
    newItem = Item.objects.create(itemname= request.POST['itemname'] , addedBy = User.objects.get(id= request.session['logId']))
    return redirect("/homepage")

def itemInfo(request, itemid):
    context = {
        'item': Item.objects.get(id=itemid)
    }
    return render(request, 'iteminfo.html', context)

def delete(request, itemid):
    deleteme = Item.objects.get(id=itemid)
    deleteme.delete()
    return redirect("/homepage")

def faved(request, itemid):
    userlog = User.objects.get(id= request.session['logId'])
    itemliking = Item.objects.get(id=itemid)
    itemliking.favoritedby.add(userlog)

    return redirect("/likeditem")

def unfaved(request, itemid):
    userlog = User.objects.get(id= request.session['logId'])
    itemliking = Item.objects.get(id=itemid)
    itemliking.favoritedby.remove(userlog)

    return redirect("/homepage")

def likeditem(request):
    return redirect("/homepage")

# Create your views here.

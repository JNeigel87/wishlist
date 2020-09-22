from django.db import models
import re

class UserManager(models.Manager):
    def baseValidator(self, postData):
        errors = {}
        resultedFilter = User.objects.filter(username = postData["username"])
        print(resultedFilter)
        if len(postData['name']) == 0:
            errors['namerequired'] = "Name is required!"
        if len(postData['username']) == 0:
            errors['usernamerequired'] = "Username is required!"
        if len(resultedFilter)>0:
            errors['usernameused'] = "This username is already being used!"
        if len(postData['password']) == 0:
            errors['passwordrequired'] = "Password is required!"
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pwmatch'] = "Confirm Password must match!!"
        return errors

    def loginValidation(self, postData):
        errors = {}
        resultedFilter = User.objects.filter(username=postData['username'])
        if len(postData['username']) == 0:
            errors['usernamerequired'] = "Username is required!"
            return errors
        elif  len(resultedFilter) == 0:
            errors['invaliduser'] = "Username not found! Please Register to login!" 
            
        else:
            if len(postData['password']) == 0:
                errors['passwordrequired'] = "Password is required!"
            elif postData['password'] != resultedFilter[0].password:
                errors['invalidpassword'] = "Invalid Password"
        return errors

class ItemManager(models.Manager):
    def itemvalidation(self, postData):
        errors = {}
        resultFilter = User.objects.filter(username = postData["itemname"])
        print(resultFilter)
        if len(postData['itemname']) == 0:
            errors['itemnamerequired'] = "An item ame is required!"
        if len(resultFilter)>0:
            errors['itemnameused'] = "This item was previously added!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
# Create your models here.

class Item(models.Model):
    itemname = models.CharField(max_length=45)
    addedBy = models.ForeignKey(User, related_name="item_added", on_delete=models.CASCADE)
    favoritedby = models.ManyToManyField(User, related_name="faved_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
from django.db import models

# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='images/')
    gold = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.username} - {self.gold}"
    


class Store(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    achived = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    code = models.CharField(max_length=50,blank=True,null=True)
    product_type = models.BooleanField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.product_name} - {self.product_price} - {self.achived}"

class MoneyCode(models.Model):
    code = models.CharField(max_length=50)
    money_value = models.IntegerField(default=100)
    achived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.money_value} - {self.achived}"


    

class Galeri(models.Model):
    image = models.ImageField(upload_to='uploads/') 

    def __str__(self):
        return f"{self.image}"
    

class Quiz(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200,blank=True,null=True)
    questions = models.JSONField(default=list)
    status = models.BooleanField(default=False)
    score = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.title



class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_type = models.CharField(max_length=200,blank=True,null=True)
    product_price = models.IntegerField(blank=True,null=True)
    product_link = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self):
        return f"{self.product_name} - {self.product_price}"


    




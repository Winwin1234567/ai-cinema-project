from django.db import models
from datetime import datetime
import uuid 
# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=200)
   
    def __str__(self):
       return self.name



class Movie(models.Model):
  moviename = models.CharField(max_length=255)
  moviedescription = models.CharField(max_length=255)
 
  moviecategories_id = models.ForeignKey(Categories,on_delete=models.SET_NULL,null=True,related_name='categories')
  movie_showdate = models.DateTimeField(null=True, blank=True)
  movie_image = models.ImageField(null=True,blank=True,upload_to='Movies/')
  movie_status = models.BooleanField(default=False)

  def __str__(self):
        return self.moviename
  



class Seatname(models.Model):
  seatplace = models.CharField(max_length=255)
  
  seatstatus = models.BooleanField(default=False)
  
  moviename = models.CharField(max_length=255)
  movie_id = models.ForeignKey(Movie,on_delete=models.SET_NULL,null=True,related_name='movies')
  
  seatstatus_completed = models.BooleanField(default=False)

  
  
  def __str__(self):
        return self.seatplace
  

 
class Ticketprice(models.Model):
  
  ticketcost = models.IntegerField(null=True)

  
  moviename = models.CharField(max_length=255)
  ticketmovie_id = models.ForeignKey(Movie,on_delete=models.SET_NULL,null=True,related_name='ticketmovies')
  
  

  
  
  def __str__(self):
        return self.moviename 
  


class Customer(models.Model):
   
  moviename = models.CharField(max_length=255)
  customermovie_id = models.ForeignKey(Movie,on_delete=models.SET_NULL,null=True,related_name='customermovies')
  seatplace = models.CharField(max_length=255)
  customer_id_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
  total_cost = models.IntegerField(default=0)
  customer_name = models.CharField(null=True,blank=True,max_length=255)
  phone = models.CharField(null=True,blank=True,max_length=200)
  cusmovie_showdate = models.DateTimeField(null=True, blank=True)
  moneystatus_completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=datetime.now)

  
  
  def __str__(self):
        return self.customer_name
from django.shortcuts import render,get_object_or_404

from .models import *
#from datetime import datetime
import uuid 
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def mocategories(request):
    mocategories = Categories.objects.all().order_by('-id')
    allmovielist = Movie.objects.all().order_by('-id')

    paginator = Paginator(allmovielist,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,'mocategories.html',{'mocategories':mocategories,'allmovielist':allmovielist,'posts':page_obj})
    

def movielist(request,foo):
    cat = Categories.objects.get(name = foo)
    movielist = Movie.objects.filter(moviecategories_id = cat).order_by('-id')
    
    paginator = Paginator(movielist,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'mocategories.html',{'cat':cat,'movielist':movielist,'movielistcat':page_obj})



def check_id(request,check_mid):
    
    movie = get_object_or_404(Movie,id=check_mid)
    
    ticket_id = uuid.uuid4() 
    
    myemptyseatstatus = Seatname.objects.all().values()

    myticketprice = Ticketprice.objects.all().values()
    
    if Seatname.objects.filter(movie_id_id = movie.id,moviename = movie.moviename,seatplace = 'sc',seatstatus_completed = False).exists():
    
     
     return render(request,'emptyseats.html',{'id':movie.id,'name':movie.moviename,'moviedate':movie.movie_showdate,'movieimage':movie.movie_image,'myemptyseatstatus':myemptyseatstatus,'myticketprice':myticketprice,'ticketid':ticket_id})
    elif Seatname.objects.filter(movie_id_id = movie.id,seatplace = 'sc',moviename = movie.moviename,seatstatus_completed = True).exists(): 
     return render(request,'fullseat.html')
    else:
     return render(request,'notseatget.html',{'id':movie.id,'name':movie.moviename})  
    

    
def seatupdate(request):
    myseatupdate = Seatname.objects.all().values()
    
   # o = json.dumps({"ticket_ids": ticket_ids}, default=str)
    context ={}
    if request.method == "POST":
      movie_id = request.POST.get('movie_id')
      seatplace_list = request.POST.getlist('boxes')

      
      coursename = request.POST.get('coursename',None)
      coursename3 = request.POST.get('coursename3',None)
      movie_sid = movie_id
      movie_sname = request.POST.get('movie_name',None)
      movie_sdate = request.POST.get('moviedate',None)
      ticket_id =  request.POST.get('ticketid',None)
      customername = request.POST.get('customername',None)
      phone =  request.POST.get('phone',None)
    
      context['coursename'] = coursename
      context['coursename3'] = coursename3
      context['movie_sid'] = movie_sid
      context['movie_sname'] = movie_sname
      context['movie_sdate'] = movie_sdate
      context['customername'] = customername
      context['phone'] = phone
      context['ticket_id'] = ticket_id
      
      for x in seatplace_list:
          Seatname.objects.filter(movie_id=movie_id,seatplace=x).update(seatstatus=True)

      messages.success(request,'Your tickets are here now!Please confirm it!')            
      return render(request,'custticket.html',context)
    return render(request, 'emptyseats.html',{'myseatupdate':myseatupdate}) 


def customer_create(request):
   
    

    if request.method == "POST":
        
        customermovie_id = request.POST.get('movieid')
        moviename = request.POST.get('moviename') 

        movie_sdate = request.POST.get('moviedate')

        #cusmovie_sdate = datetime.strptime( movie_sdate,"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        seatname = request.POST.get ('seatname')
       
        totalcost = request.POST.get('totalcost')
        
        ticket_id = request.POST.get('ticket_id')
        customername = request.POST.get('customername')
        customerphone = request.POST.get('customerphone')   
        idseatname = [x.strip() for x in seatname.split(',')][:-1]
        
        if not all([customermovie_id,moviename,seatname,totalcost,ticket_id,customername,customerphone]):
           return render(request,'notseatget.html')
        else:
            for i in idseatname:
                Seatname.objects.filter(movie_id_id=customermovie_id,seatplace=i).update(seatstatus_completed=True)
                
                obj , created = Customer.objects.get_or_create(
                customer_id_id=ticket_id,
                defaults={'moviename':moviename, 'customermovie_id_id':customermovie_id,'seatplace':seatname,'customer_id_id':ticket_id,'total_cost':totalcost,'customer_name':customername,'phone':customerphone,'cusmovie_showdate':movie_sdate}
                 )
               
                customer1 =Customer.objects.filter(moviename=moviename,customermovie_id_id=customermovie_id,customer_id_id=ticket_id)
            messages.success(request,'Your tickets confirmation is completed!')   
            return render(request,'ticketinfo.html',{'customer1':customer1,'moviedate':movie_sdate})

    
def trace(request):
   trace = request.GET.get('search')
   if trace:
      ticket_id = Customer.objects.filter(
         Q(customer_id_id__icontains=trace)
      )
      messages.success(request,'Your tracking ticket is here!') 
      return render(request,'trace.html',{'ticket_id':ticket_id})
   else:
      trace1 = 'Please trace your ticket status after paying money.Thank you!'
      return render(request,'trace.html',{'trace1':trace1})
   

def generate():
  from random import randrange
  num = randrange(0,12)
  return num

def output(request):
    context = {
        'number': generate()
    }
    return render(request,'fortuneteller.html',context)



#static pages

def home(request):
    
    return render(request,'index.html')

def aboutus(request):
    
    return render(request,'aboutus.html')


def map(request):
    
    return render(request,'map.html')



def readme(request):
    
    return render(request,'readme.html')
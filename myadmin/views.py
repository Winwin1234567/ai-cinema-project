from django.shortcuts import render,redirect,get_object_or_404
from mymovie.models import *
# Create your views here.
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import  login_required,permission_required
import os
#login

def login_views(request):
    if request.method == "GET":
        return render(request,'adminlogin.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username ='admin',password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"You are logged in as "+ username)
            return redirect('/myadmin/mocategoriesadmindashboard/')
        
        
        userm = authenticate(request,username='manager',password=password)
        
        if userm is not None:
            login(request,userm)
            messages.success(request,"You are logged in as "+ username + " so you can't access to dashboard")
            return redirect('/myadmin/mocategoriesadmin/')
        userc = authenticate(request,username='cashier',password=password)
        if userc is not None:
            login(request,userc)
            messages.success(request,"You are logged in as "+ username +" so you can't access to dashboard")
            return redirect('/myadmin/customerlist/')
        
        else:
            messages.error(request,"Invalid username or password!")
            return redirect('login')


       

def logout_views(request):
    logout(request)
    messages.error(request,"You are logged out!")
    return redirect('/login/')


#movie
@permission_required('mymovie.view_movie',login_url='login')
def mocategoriesadmin(request):
    
    allmovielist = Movie.objects.all().order_by('-id')

    paginator = Paginator(allmovielist,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,'movielist.html',{'allmovielist':page_obj})
    
@permission_required('mymovie.add_movie',login_url='login')
def movie_create(request):
    if request.method == "GET":
      mocategories = Categories.objects.all()
      
      return render(request,'createmovie.html',{'moviecategories':mocategories})

    if request.method == "POST":
        
        moviename = request.POST.get('moviename')
        moviedescription = request.POST.get('moviedescription')
        
        moviecategories_id = request.POST.get('moviecategories_id')
        movie_showdate = request.POST.get('movie_showdate')
        movie_image = request.FILES.get('movie_image')
        movie_status =  request.POST.get('movie_status') == 'on'
        movie_create = Movie(moviename=moviename,moviedescription=moviedescription,moviecategories_id_id=moviecategories_id,movie_showdate=movie_showdate,movie_image=movie_image,movie_status=movie_status)
        movie_create.save()
        
        messages.success(request,'Movie created successfully!')
       

        
        return redirect('mocategoriesadmin')
    return render(request,'createmovie.html')

@permission_required('mymovie.change_movie',login_url='login')
def movielist_update(request,update_id):
    movielistu = get_object_or_404(Movie,id=update_id)
    if request.method == "GET":
      mocategories = Categories.objects.all()
      
     
    
    if request.method == "POST":
        
        movielistu.moviename = request.POST.get('moviename')
        movielistu.moviedescription = request.POST.get('moviedescription')
        movielistu.moviecategories_id_id= request.POST.get('moviecategories_id')
        movielistu.movie_showdate = request.POST.get('movie_showdate')
       
        movielistu.movie_status =  request.POST.get('movie_status') == 'on'
       
       


        if len(request.FILES) != 0:
           if len(movielistu.movie_image) > 0:
            os.remove(movielistu.movie_image.path)

            movielistu.movie_image = request.FILES.get('movie_image')

       
        movielistu.save()
        
        messages.info(request,'Movie updated successfully!')

        
        return redirect('mocategoriesadmin')
    return render(request,'createmovie.html',{'movielistu':movielistu,'moviecategories':mocategories})

     

@permission_required('mymovie.delete_movie',login_url='login')
def delete_movielist(request, movielist_id):
     allmovielistdel = get_object_or_404(Movie,id=movielist_id)
     
     if allmovielistdel.movie_image:
        if os.path.isfile(allmovielistdel.movie_image.path):
           os.remove(allmovielistdel.movie_image.path)

     
     allmovielistdel.delete()
     messages.error(request,'Movie deleted successfully!')
     return redirect('mocategoriesadmin')

#seat
@permission_required('mymovie.view_seatname',login_url='login')
def seatlist(request):
    
    allseatlist = Seatname.objects.all().order_by('-id')

    paginator = Paginator(allseatlist,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,'seatlist.html',{'allseatlist':page_obj})

@permission_required('mymovie.add_seatname',login_url='login')
def seat_create(request):
    if request.method == "GET":
      movieid = Movie.objects.all().order_by('-id')
      
      return render(request,'createseat.html',{'movieid':movieid})

    if request.method == "POST":
        
        seatplace = request.POST.get('seatplace')
        seatstatus = request.POST.get('seatstatus') == 'on'
        moviename = request.POST.get('moviename')
        movie_id = request.POST.get('movie_id')
        seatstatus_completed = request.POST.get('seatstatus_completed') == 'on'
        
        seat_create = Seatname(seatplace=seatplace,seatstatus=seatstatus,moviename=moviename,movie_id_id=movie_id,seatstatus_completed=seatstatus_completed)
        seat_create.save()
        
        messages.success(request,'Seat created successfully!')

        
        return redirect('seat_create')
    return render(request,'createseat.html')

@permission_required('mymovie.change_seatname',login_url='login')
def seatlist_update(request,update_id):
    seatlistu = get_object_or_404(Seatname,id=update_id)
    if request.method == "GET":
      movieid = Movie.objects.all()
      
     
    
    if request.method == "POST":
        
        seatlistu.seatplace = request.POST.get('seatplace')
        seatlistu.seatstatus = request.POST.get('seatstatus') == 'on'
        seatlistu.moviename= request.POST.get('moviename')
        seatlistu.movie_id_id = request.POST.get('movie_id')
       
        seatlistu.seatstatus_completed =  request.POST.get('seatstatus_completed') == 'on'
       
        seatlistu.save()
        
       
        messages.info(request,'Seat updated successfully!')
        
        return redirect('seatlist')
    return render(request,'createseat.html',{'seatlistu':seatlistu,'movieid':movieid})



@permission_required('mymovie.delete_seatname',login_url='login')
def delete_seatlist(request, seatlist_id):
     allseatlistdel = Seatname.objects.filter(id = seatlist_id)

     
     allseatlistdel.delete()
     messages.error(request,'Seat deleted successfully!')
     return redirect('seatlist')


#ticketprice
@permission_required('mymovie.view_ticketprice',login_url='login')
def ticketpricelist(request):
    
    ticketpricelistlist = Ticketprice.objects.all().order_by('-id')

   
    paginator = Paginator(ticketpricelistlist,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'ticketpricelist.html',{'ticketpricelistlist':page_obj})


@permission_required('mymovie.add_ticketprice',login_url='login')
def ticketprice_create(request):
    if request.method == "GET":
      ticketmovieid = Movie.objects.all().order_by('-id')
      
      return render(request,'createticketprice.html',{'ticketmovieid':ticketmovieid})

    if request.method == "POST":
        
        ticketcost = request.POST.get('ticketcost')
        
        moviename = request.POST.get('moviename')
        ticketmovie_id = request.POST.get('ticketmovie_id')
        
        
        ticketprice_create = Ticketprice(ticketcost=ticketcost,moviename=moviename,ticketmovie_id_id=ticketmovie_id)
        ticketprice_create.save()
        
        

        messages.success(request,'Ticket price created successfully!')
        return redirect('ticketpricelist')
    return render(request,'createticketprice.html')


@permission_required('mymovie.change_ticketprice',login_url='login')
def ticketprice_update(request,update_id):
    ticketcostu = get_object_or_404(Ticketprice,id=update_id)
    if request.method == "GET":
      ticketmovieid = Movie.objects.all()
      
     
    
    if request.method == "POST":
        
        ticketcostu.ticketcost = request.POST.get('ticketcost')
        
        ticketcostu.moviename= request.POST.get('moviename')
        ticketcostu.ticketmovie_id_id = request.POST.get('ticketmovie_id')
       
        
        ticketcostu.save()
        
       

        messages.info(request,'Ticket price updated successfully!')
        return redirect('ticketpricelist')
    return render(request,'createticketprice.html',{'ticketcostu':ticketcostu,'ticketmovieid':ticketmovieid})


@permission_required('mymovie.delete_ticketprice',login_url='login')

def delete_ticketpricelist(request, ticketpricelist_id):
     ticketpricelistdel = Ticketprice.objects.filter(id = ticketpricelist_id)

     
     ticketpricelistdel.delete()
     messages.error(request,'Ticket price deleted successfully!')
     return redirect('ticketpricelist')

#customer
@permission_required('mymovie.view_customer',login_url='login')
def customerlist(request):
    
    allcustomerlist = Customer.objects.all().order_by('-created_at')


    paginator = Paginator(allcustomerlist,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'customerlist.html',{'allcustomerlist':page_obj})

@permission_required('mymovie.view_customer',login_url='login')
def customerdetail(request, customerdetail_id):
     customer_detail = Customer.objects.filter(customer_id_id = customerdetail_id)

     
     

     return render(request,'customerdetail.html',{'customer_detail':customer_detail})


@permission_required('mymovie.change_customer',login_url='login')
def customerlist_update(request,update_id):
    customerlistu = get_object_or_404(Customer,customer_id_id=update_id)
    if request.method == "GET":
      cusmovieid = Movie.objects.all()
      
     
    
    if request.method == "POST":
        
        customerlistu.moviename = request.POST.get('moviename')
        customerlistu.customermovie_id_id = request.POST.get('customermovie_id') 
        customerlistu.seatplace= request.POST.get('seatplace')
        customerlistu. customer_id_id = request.POST.get('customer_id_id')
        customerlistu.total_cost= request.POST.get('total_cost')
        customerlistu.customer_name= request.POST.get('customer_name')
        customerlistu.phone= request.POST.get('phone')
        customerlistu.cusmovie_showdate = request.POST.get('cusmovie_showdate')
        customerlistu.moneystatus_completed  =  request.POST.get('moneystatus_completed') == 'on'
        customerlistu.created_at =  request.POST.get('created_at')
        customerlistu.save()
        
        messages.info(request,'Customer updated successfully!')

        
        return redirect('customerlist')
    return render(request,'customerlistupdate.html',{'customerlistu':customerlistu,'cusmovieid':cusmovieid})


@permission_required('mymovie.delete_customer',login_url='login')
def delete_customerlist(request, customerlist_id):
     customerlistdel = Customer.objects.filter(customer_id_id = customerlist_id)

     
     customerlistdel.delete()
     messages.error(request,'Customer deleted successfully!')
     return redirect('customerlist')

#admindashboard

@login_required(login_url='login')
def mocategoriesadmindashboard(request):
    

    mocategories = Categories.objects.all().order_by('-id')
    allmovielist = Movie.objects.all().order_by('-id')

    paginator = Paginator(allmovielist,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total = Customer.objects.aggregate(Sum('total_cost'))['total_cost__sum']
    movie_count = Movie.objects.count()
    showedmovie_count = Movie.objects.filter(movie_status = True).count()
    
    return render(request,'admindashboard.html',{'mocategories':mocategories,'allmovielist':allmovielist,'posts':page_obj,'total_cost':total,'moviecount':movie_count,'showedmoviecount':showedmovie_count})


@login_required(login_url='login')
def mocategoriesadmindashboardnewmovie(request):
    

    mocategories = Categories.objects.all().order_by('-id')
    allmovielist = Movie.objects.all().order_by('id')

    paginator = Paginator(allmovielist,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total = Customer.objects.aggregate(Sum('total_cost'))['total_cost__sum']
    movie_count = Movie.objects.count()
    showedmovie_count = Movie.objects.filter(movie_status = True).count()
    
    return render(request,'admindashboardnewmovie.html',{'mocategories':mocategories,'allmovielist':allmovielist,'newmovie':page_obj,'total_cost':total,'moviecount':movie_count,'showedmoviecount':showedmovie_count})




@login_required(login_url='login')
def check_total(request,check_total):
    

    mocategories = Categories.objects.all().order_by('-id')
    allmovielist = Movie.objects.all().order_by('-id')

    paginator = Paginator(allmovielist,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total = Customer.objects.aggregate(Sum('total_cost'))['total_cost__sum']

    totaleachmovie = Customer.objects.filter(customermovie_id_id = check_total).aggregate(Sum('total_cost'))['total_cost__sum']

    cusmoviename = Movie.objects.filter(id = check_total)

    movie_count = Movie.objects.count()
    showedmovie_count = Movie.objects.filter(movie_status = True).count()
   
    return render(request,'admindashboard.html',{'mocategories':mocategories,'allmovielist':allmovielist,'posts':page_obj,'total_cost':total,'totaleachmovie':totaleachmovie,'cusmoviename':cusmoviename,'moviecount':movie_count,'showedmoviecount':showedmovie_count})


   
    

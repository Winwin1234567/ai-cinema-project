from django.urls import path
from . import views


urlpatterns = [
    
    
    #movie
   path('mocategoriesadmin/',views.mocategoriesadmin,name='mocategoriesadmin'),
   path('movie_create/create/',views.movie_create,name='movie_create'),
   path('delete_movielist/<int:movielist_id>',views.delete_movielist,name='delete_movielist'),
   path('movielist_update/<int:update_id>',views.movielist_update,name='movielist_update'),

   #seat

    path('seatlist/',views.seatlist,name='seatlist'),
    path('seat_create/create/',views.seat_create,name='seat_create'),
    path('seatlist_update/<int:update_id>',views.seatlist_update,name='seatlist_update'),

    path('delete_seatlist/<int:seatlist_id>',views.delete_seatlist,name='delete_seatlist'),

    #ticketprice
    path('ticketpricelist/',views.ticketpricelist,name='ticketpricelist'),
    path('ticketprice_create/create/',views.ticketprice_create,name='ticketprice_create'),
     path('ticketpricelist_update/<int:update_id>',views.ticketprice_update,name='ticketpricelist_update'),
     path('delete_ticketpricelist/<int:ticketpricelist_id>',views.delete_ticketpricelist,name='delete_ticketpricelist'),

     #customerlist
     path('customerlist/',views.customerlist,name='customerlist'),
     path('customerdetail/<uuid:customerdetail_id>',views.customerdetail,name='customerdetail'),
     path('customerlist_update/<uuid:update_id>',views.customerlist_update,name='customerlist_update'),
     path('delete_customerlist/<uuid:customerlist_id>',views.delete_customerlist,name='delete_customerlist'),

     #admindashboard
      path('mocategoriesadmindashboard/',views.mocategoriesadmindashboard,name='mocategoriesadmindashboard'),
      path('mocategoriesadmindashboardnewmovie/',views.mocategoriesadmindashboardnewmovie,name='mocategoriesadmindashboardnewmovie'),
      path('check_total/<int:check_total>/', views.check_total, name='check_total'),
]     

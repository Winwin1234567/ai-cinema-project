from django.urls import path
from . import views

urlpatterns = [
    #buy seat
   path('mocategories/',views.mocategories,name='mocategories'),
    path('movielist/<str:foo>',views.movielist,name='movielist'),
    path('check_id/<int:check_mid>/', views.check_id, name='check_id'),
    path('seatupdate/', views.seatupdate, name='seatupdate'),
    path('customer_create/', views.customer_create, name='customer_create'),
     path('trace/', views.trace, name='trace'),
     path('output/',views.output,name='output'),

   #static pages
   path('home/',views.home,name='home'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('map/',views.map,name='map'),
    path('readme/',views.readme,name='readme'),
]
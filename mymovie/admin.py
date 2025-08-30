from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Categories)
admin.site.register(Movie)
admin.site.register(Seatname)
admin.site.register(Ticketprice)
admin.site.register(Customer)
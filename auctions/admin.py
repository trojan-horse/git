from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Bid)
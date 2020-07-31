from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *

from datetime import datetime


def index(request):

    return render(request, "auctions/index.html", {
        "idk": AuctionListing.objects.all(),
        'user_id': request.user.id,
        "bids": Bid.objects.all(),
        "empty": not Bid.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createlisting(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        current_price = starting_bid
        date_created =  datetime.now()

        try:
            category = Category.objects.get(pk=int(request.POST["category"]))
        except:
            category = ''
        image = request.POST["image"]
        user = User.objects.get(pk=request.user.id)

        AuctionListing(current_price=current_price, user=user, title=title, description=description, starting_bid=starting_bid, category=category, image=image, date_created=date_created).save()


    return render(request, "auctions/createlisting.html", {
        'categories': Category.objects.all()
    })

def listing(request, listing_id):
    try:
        user = User.objects.get(pk=request.user.id)
    except:
        user= 'guest'
    listing = AuctionListing.objects.get(pk=int(listing_id))
    bidlist = [bid.bid for bid in Bid.objects.all().filter(listing=listing_id)]
    time = datetime.now()
    message = ''

    userwl = WatchList.objects.all().filter(user=request.user.id)
    wlitems = []
    for item in userwl:
        wlitems.append(item.listing)

    try:
        winner = Bid.objects.get(bid=listing.current_price, listing=listing_id)
    except:
        winner = ''

    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            if request.POST.get("save"):
                WatchList(user=user, listing=listing).save()
                return HttpResponseRedirect(f'{listing_id}')
            elif request.POST.get('remove'):
                WatchList.objects.all().filter(listing=listing).delete()
                return HttpResponseRedirect(f'{listing_id}')
            elif request.POST.get('close'):
                AuctionListing.objects.filter(id=listing_id).update(active=False)
                return HttpResponseRedirect(f'{listing_id}')
            elif request.POST.get('bid'):
                newbid = int(request.POST["bid"])
                if (newbid >= listing.current_price):
                        Bid(owner=user, listing=listing, bid=newbid, latest_bid_time=time).save()
                        AuctionListing.objects.filter(id=listing_id).update(current_price=newbid)
                        message = ''
                        return HttpResponseRedirect(f'{listing_id}')
                else:
                    message = "Bid must be higher than current price."
        elif request.POST.get("form_type") == 'comment':
            comment = request.POST["comment"]

            Comment(user=user, listing=listing, comment=comment, time=time).save()

    return render(request, "auctions/listing.html", {
        "in_wl": listing in wlitems,
        "listing_id": listing_id,
        "detail": AuctionListing.objects.get(id=listing_id),
        "comments": Comment.objects.all().filter(listing=listing_id),
        "current_price": listing.current_price,
        'message': message,
        'winner': winner,
        "number_of_bids": len(bidlist)
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'items': WatchList.objects.all().filter(user=request.user.id),
        'empty': not WatchList.objects.all().filter(user=request.user.id)
    })

def categories(request, category_id):
    return render(request, "auctions/categories.html", {
        'category': Category.objects.get(id=category_id),
        'items': AuctionListing.objects.all().filter(category=int(category_id))
    })

def category_index(request):
    return render(request, "auctions/category_index.html", {
        'categories': Category.objects.all()
    })

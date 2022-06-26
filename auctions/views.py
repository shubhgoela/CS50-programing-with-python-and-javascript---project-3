from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from .models import User, Listing, Bid, Category, Comment, Watchlist
from .forms import BidForm, CommentForm, ListingForm, WatchlistForm

def index(request):
        return render(request, "auctions/index.html",{
            "listing_type" : "ACTIVE",
            "listings": (Listing.objects.filter(status = "BID") | Listing.objects.filter(status = "ACTIVE")).reverse()[ ::-1]
        })

@login_required(login_url='/')
def index2(request):
    return render(request, "auctions/index.html",{
        "listing_type" : "ACTIVE",
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.count(),
        "listings": (Listing.objects.filter(status = "BID") | Listing.objects.filter(status = "ACTIVE")).reverse()[ ::-1]
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
            return HttpResponseRedirect(reverse("index2"))
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
        return HttpResponseRedirect(reverse("index2"))
    else:
        return render(request, "auctions/register.html")

def newlisting(request):
    if request.method == "POST":
        print(request.POST)
        form = ListingForm(request.POST)
        listing = form.save(commit = False)
        listing.user = User.objects.get(pk = request.POST['user'])
        listing.save()
        form.save_m2m()
        if form.is_valid():
            print('clean')
            return HttpResponseRedirect(reverse("index2"))
        else:
            print(form)
    form = ListingForm(initial={'user': User.objects.get(pk = request.session['_auth_user_id'])})
    return render(request, "auctions/newlisting.html", {
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "form":form
    })

@login_required(login_url='/login')
def listing(request, id):
    Watchlistform = WatchlistForm(initial={
        'user': User.objects.get(pk = request.session['_auth_user_id']),
        'listing': Listing.objects.get(pk = id)
    })
    Bidform = BidForm(initial={
        'user': User.objects.get(pk = request.session['_auth_user_id']),
        'listing': Listing.objects.get(pk = id)
    })
    Commentform = CommentForm(initial={
        'user': User.objects.get(pk = request.session['_auth_user_id']),
        'listing': Listing.objects.get(pk = id)
    })
    if request.method == "POST":
        print("User id : ", request.session['_auth_user_id'])
        print("Request : ", request.POST)
        if 'comment' in request.POST.keys():
            c1 = CommentForm(request.POST)
            c1.save()
            '''return render(request, "auctions/listing.html",{
                "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                "listing": Listing.objects.get(pk = id),
                "bidform":Bidform,
                "commentform":Commentform,
                "watchlistform" : Watchlistform,
                "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                "comments" : Listing.objects.get(pk = id).comments.all(),
                "bid_count" : Listing.objects.get(pk = id).bids.all().count()
            })'''
            return HttpResponseRedirect(f"/listing/{id}",{
                "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                "listing": Listing.objects.get(pk = id),
                "bidform":Bidform,
                "commentform":Commentform,
                "watchlistform" : Watchlistform,
                "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                "comments" : Listing.objects.get(pk = id).comments.all(),
                "bid_count" : Listing.objects.get(pk = id).bids.all().count()
            })
        elif 'watchlist' in request.POST.keys():
            if request.POST['watchlist'] == 'Add':
                w1 = WatchlistForm(request.POST)
                w1.save()
                print("New watchlist object created")
                return HttpResponseRedirect(f"/listing/{id}",{
                    "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                    "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
                    "listing": Listing.objects.get(pk = id),
                    "bidform":Bidform,
                    "commentform":Commentform,
                    "watchlistform" : Watchlistform,
                    "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                    "comments" : Listing.objects.get(pk = id).comments.all(),
                    "bid_count" : Listing.objects.get(pk = id).bids.all().count()
                })
            else:
                w1 = Watchlist.objects.get(user = request.POST['user'], listing=request.POST['listing']).delete()
                print("Watchlist object deleted")
                print(w1)
                return HttpResponseRedirect(f"/listing/{id}",{
                    "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                    "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
                    "listing": Listing.objects.get(pk = id),
                    "bidform":Bidform,
                    "commentform":Commentform,
                    "watchlistform" : Watchlistform,
                    "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                    "comments" : Listing.objects.get(pk = id).comments.all(),
                    "bid_count" : Listing.objects.get(pk = id).bids.all().count()
                })
        elif "bid" in request.POST.keys():
            bidform = BidForm(request.POST)
            print(bidform)
            if bidform.is_valid():
                bidform.save()
                l = Listing.objects.get(pk = request.POST["listing"])
                l.price = request.POST["bid"]
                l.status = "BID"
                l.save()
                return HttpResponseRedirect(f"/listing/{id}",{
                    "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                    "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
                    "listing": Listing.objects.get(pk = id),
                    "bidform":Bidform,
                    "commentform":Commentform,
                    "watchlistform" : Watchlistform,
                    "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                    "comments" : Listing.objects.get(pk = id).comments.all(),
                    "bid_count" : Listing.objects.get(pk = id).bids.all().count()
                })
            else:
                return render(request,"auctions/listing.html",{
                    "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
                    "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
                    "listing": Listing.objects.get(pk = id),
                    "bidform":bidform,
                    "commentform":Commentform,
                    "watchlistform" : Watchlistform,
                    "current_bid": Listing.objects.get(pk = id).bids.all().last(),
                    "comments" : Listing.objects.get(pk = id).comments.all(),
                    "bid_count" : Listing.objects.get(pk = id).bids.all().count()
                })
        else:
          print(request.POST) 
          listing = Listing.objects.get(pk = request.POST['listing'])
          listing.status = request.POST['status']
          listing.save()
          return HttpResponseRedirect(f"/listing/{id}",{
              "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
              "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
              "listing": Listing.objects.get(pk = id),
              "bidform":Bidform,
              "commentform":Commentform,
              "watchlistform" : Watchlistform,
              "current_bid": Listing.objects.get(pk = id).bids.all().last(),
              "comments" : Listing.objects.get(pk = id).comments.all(),
              "bid_count" : Listing.objects.get(pk = id).bids.all().count()
          })


    return render(request, "auctions/listing.html",{
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "watchlist" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().filter(listing = id).count()>0,
        "listing": Listing.objects.get(pk = id),
        "bidform":Bidform,
        "commentform":Commentform,
        "watchlistform" : Watchlistform,
        "current_bid": Listing.objects.get(pk = id).bids.all().last(),
        "comments" : Listing.objects.get(pk = id).comments.all(),
        "bid_count" : Listing.objects.get(pk = id).bids.all().count()
    })

@login_required(login_url='/login')
def watchlist(request):
    wlist = User.objects.get(pk = request.session['_auth_user_id']).watchlist.all()             
    listings = []
    for i in wlist: listings.append(i.listing)
    return render(request, "auctions/index.html", {
        "listing_type" : "WATCHLIST",
        "watchlistcount" : wlist.count(),
        "listings" : listings
    })

def category(request):
    category = Category.objects.all()
    return render(request, "auctions/category.html",{
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "categories" : category 
    })

def listcategory(request, id):
    l = Category.objects.get(code = id).cat_listings.all()
    listings = []
    for i in l:
        if i.status != "CLOSED":
            listings.append(i)
    print(request.session['_auth_user_id'])
    return render(request,"auctions/index.html",{
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "listing_type" : Category.objects.get(code = id).category,
        "listings" : listings
    })

def bids(request):
    listing = Listing.objects.filter(status = "CLOSED")
    bid_list = []
    print(listing)
    for i in listing:
        if i.bids.all().count() > 0:
            print(i.bids.all().last())
            print(i.bids.all().last().user.id)
            print(i.bids.all().last().user.id == int(request.session["_auth_user_id"]))
            if i.bids.all().last().user.id == int(request.session["_auth_user_id"]):
                bid_list.append(i)
    #request.session['bid_set'] = set(request.session["bid_list"])
    print(bid_list)
    return render(request, "auctions/index.html",{
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "listing_type" : "bids",
        "listings" : bid_list
    })

def userlistings(request):
    return render(request, "auctions/index.html",{
        "watchlistcount" : User.objects.get(pk = request.session['_auth_user_id']).watchlist.all().count(),
        "listing_type" : "self",
        "listings" : Listing.objects.filter(user = request.session['_auth_user_id'])
    })
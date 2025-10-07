from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Item, Bid

CATEGORY_CHOICES = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('music', 'Music'),
    ('watches', 'Watches'),
]


class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    bid_price = forms.DecimalField(label="Bid Price")
    image_url = forms.CharField(label="Image URL")
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select,
        label="Select a Category"
    )


class BidForm(forms.Form):
    user_bid_price = forms.DecimalField(label="Enter Your Bid")


#class CloseAuctionForm(forms.Form):
#    user_bid_price = forms.DecimalField(label="Enter Your Bid")


def index(request):
    items = Item.objects.all()
    return render(request, "auctions/index.html", {
        "items": items,
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


def listing(request):
    return HttpResponse("Listing here... (under construction)")

@login_required
def item(request, listing_id):
    user = request.user
    item = Item.objects.get(id=listing_id)

    if request.method == "POST":
        if "submit_watchlist" in request.POST:
            add = int(request.POST["add"])
            if add == 0:
                user.favorites.add(item)
            else:
                user.favorites.remove(item)
            return HttpResponseRedirect(reverse("watchlist"))
        elif "submit_close_auction" in request.POST:
            item.onpost = 0
            item.save()
            if item.current_bidder:
                return HttpResponse(f"Auction Closed! Winner is {item.current_bidder}!")
            else:
                return HttpResponse(f"Auction Closed! No winner.")
        
        elif "submit_bid" in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                bid_item = item
                bid_user = user
                user_bid_price = form.cleaned_data["user_bid_price"]

                existing_bids = Bid.objects.filter(bid_item=item)
                if existing_bids.exists():
                    max_bid_price = existing_bids.order_by('-user_bid_price').first().user_bid_price
                else:
                    max_bid_price = 0

                if user_bid_price > max_bid_price and user_bid_price >= item.bid_price:
                    max_bid_price = user_bid_price
                    item.current_bid_price = max_bid_price
                    item.current_bidder = user.username
                    item.save()
                    bid = Bid(bid_item = bid_item, bid_user=bid_user, user_bid_price=user_bid_price, max_bid_price=max_bid_price)
                    bid.save()
                    return HttpResponse(f"Successfully bid by {user.username} at bid price of ${bid.user_bid_price}!!")
                else:
                    return HttpResponse(f"Unsuccessfully bid. Please place a higher price.")



    # check if item is in favorites
    is_watched = user.favorites.filter(id=listing_id).exists()
    return render(request, "auctions/item.html", {
        "item": item,
        "add": 1 if is_watched else 0,
        "form": BidForm(),
        "close_auction": 1 if user.username==item.creator else 0,
    })


@login_required
def create(request):
    
    if request.method == "POST":

        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_price = form.cleaned_data["bid_price"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            current_bid_price = bid_price
            creator = request.user

            item = Item(title=title, description=description, bid_price=bid_price, image_url=image_url, category=category, current_bid_price=current_bid_price, creator=creator)
            item.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": CreateForm()
    })

@login_required
def watchlist(request):


    user = request.user
    return render(request, "auctions/watchlist.html", {
        "user_id": user.id,
        "watchlist": user.favorites.all()
    })


def category(request):
    pass

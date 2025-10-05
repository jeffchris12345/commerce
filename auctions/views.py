from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Item

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
    # check if item is in favorites
    if user.favorites.filter(id=item.id).exists():
        return render(request, "auctions/item.html", {
            "item": item,
            "add": 1,
        })
    else:
        return render(request, "auctions/item.html", {
            "item": item,
            "add": 0,
        })


def create(request):
    
    if request.method == "POST":

        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_price = form.cleaned_data["bid_price"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            item = Item(title=title, description=description, bid_price=bid_price, image_url=image_url, category=category)
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
    if request.method == "POST":
        user = request.user
        item_id = request.POST["item_id"]
        add = request.POST["add"]
        item = Item.objects.get(id=item_id)
        if add == 0:
            user.favorites.add(item)
        else:
            user.favorites.remove(item)
        
        return render(request, "auctions/watchlist.html", {
            "user_id": user.id,
            "watchlist": user.favorites.all()
        })    

    user = request.user
    return render(request, "auctions/watchlist.html", {
        "user_id": user.id,
        "watchlist": user.favorites.all()
    })


def category(request):
    pass

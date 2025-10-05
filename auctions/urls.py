from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("listing/<int:listing_id>", views.item, name="item"),
    path("create", views.create, name="create"),
    #path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
]

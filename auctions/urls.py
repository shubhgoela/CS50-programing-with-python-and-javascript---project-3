from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings", views.index2, name="index2"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("newlisting", views.newlisting,  name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bids", views.bids, name="bids"),
    path("category/<str:id>", views.listcategory, name="listcategory"),
    path("mylistings", views.userlistings, name = "userlistings"),
    path("category", views.category, name="category")
]

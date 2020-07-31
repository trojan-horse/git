from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('categories/index', views.category_index, name='categoryindex'),
    path("categories/<int:category_id>", views.categories, name="category")
]

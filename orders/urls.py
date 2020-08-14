from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("load/", views.load, name="load"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("item/<int:id>", views.get_item, name="get_item"),
    path("checkout/", views.checkout, name="checkout"),
]

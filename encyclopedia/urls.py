from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random_title", views.random_title, name="random_title"),
    path("<str:title>", views.go_to_publication, name="go_to_publication")
]

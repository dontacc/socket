from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index-page"),
    path("<room_name>/", room, name="room_page")
]
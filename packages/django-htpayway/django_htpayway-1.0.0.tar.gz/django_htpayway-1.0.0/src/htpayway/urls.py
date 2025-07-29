from django.urls import path
from . import views


app_name = "htpayway"
urlpatterns = [
    path("begin/<transaction_id>/", views.begin, name="begin"),
    path("success/", views.success, name="success"),
    path("failure/", views.failure, name="failure"),
]

from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="contact-index"),
    path("new/", views.CreateContactView.as_view(), name="contact-create"),
    path("<uuid:id>/", views.ContactView.as_view(), name="contact-detail"),
    path("<uuid:id>/edit/", views.EditContactView.as_view(), name="contact-edit"),
]

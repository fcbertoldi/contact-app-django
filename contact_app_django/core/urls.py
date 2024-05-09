from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="contact-index"),
    path("count", views.slow_contact_count, name="contact-count"),
    path("new/", views.CreateContactView.as_view(), name="contact-create"),
    path("new/validate-email/", views.validate_email_view, name="validate-new-email"),
    path("<uuid:id>/", views.ContactView.as_view(), name="contact-detail"),
    path("<uuid:id>/edit/", views.EditContactView.as_view(), name="contact-edit"),
    path(
        "<uuid:id>/validate-email/",
        views.validate_email_view,
        name="validate-contact-email",
    ),
    path("archive/", views.start_archive, name="contact-archive"),
    path("archive/file", views.archive_file, name="contact-archive-file"),
]

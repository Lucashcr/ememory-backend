from django.urls import re_path, include, path

from emauth.views import ResetPasswordView


urlpatterns = [
    re_path(r"", include("djoser.urls")),
    re_path(r"", include("djoser.urls.authtoken")),
    path(
        "reset_password/<uid>/<token>/",
        ResetPasswordView.as_view(),
    ),
]

from django.views.generic import FormView

from emauth.forms import ResetPasswordForm


# Create your views here.
class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = "emauth/reset_password.html"

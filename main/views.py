from django.shortcuts import render
from django.views.generic import TemplateView
from openhumans.models import OpenHumansMember
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

# Create your views here.


class HomeView(TemplateView):
    template_name = "main/home.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                self.files = self.request.user.openhumansmember.list_files()
            except Exception:
                logout(request)
                return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated:
            openhumansmember = self.request.user.openhumansmember

            context.update(
                {
                    "openhumansmember": openhumansmember,
                    "files": self.files
                }
            )

        # Not logged in.
        else:
            context.update({"openhumans_login_url": OpenHumansMember.get_auth_url()})

        return context


def logout_user(request):
    """
    Logout user.
    """
    if request.method == "POST":
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    if not redirect_url:
        redirect_url = "/"
    return redirect(redirect_url)

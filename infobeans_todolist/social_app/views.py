from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name = 'social_app/test.html'

class ThanksPage(TemplateView):
    template_name = 'social_app/thanks.html'

class HomePage(TemplateView):
    template_name = "social_app/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("social_app:test"))
        return super().get(request, *args, **kwargs)

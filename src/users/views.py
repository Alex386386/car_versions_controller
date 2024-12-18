from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("cars:index")
    template_name = "users/signup.html"

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        user = form.save(commit=False)
        print(user.username, user.email, user.first_name, user.last_name)
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

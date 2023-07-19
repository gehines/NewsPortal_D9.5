from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, BasicSignupForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
class BaseRegisterView(CreateView):
    model = User
    form_class = BasicSignupForm
    success_url = '/news/'

@login_required
def upgrade_me(request):
    user = request.user
    authors_groop = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_groop.user_set.add(user)
    return redirect('/news/')

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.views import View

# Create your views here.

@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


class UserLogin(View):

    template_name = 'account/login.html'

    def get(self, request):
        form = LoginForm()

        return render(
            request,
            self.template_name,
            {
                "form": form
            }
        )

    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            
            if not user:
                return HttpResponse('Invalid login')
            elif user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        
        return render(request, self.template_name, {'form': form})

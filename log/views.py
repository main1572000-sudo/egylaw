from django.shortcuts import render,redirect
from .forms import LogForm
from django.contrib.auth import login
# from django.contrib.auth.views import LogoutView

# Create your views here.

def registration(request):
    form = LogForm()
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('archive')
    return render(request,'register.html',{'form':form})

# class CustomLogoutView(LogoutView):
#     http_method_names = ['get', 'post']
        
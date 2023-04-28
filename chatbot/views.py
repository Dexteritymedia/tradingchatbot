from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, View, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .utils import *
from .forms import SignUpForm

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super(RegisterView, self).form_valid(form)


def login(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            message.success(request, f"Welcome {username}!!!")
            return redirect("home")
        else:
            messages.info(request, f"Account does not exist please sign up or check your account details")
            form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')
    
    
class HomeTemplateView(TemplateView):
    template_name = "index.html"

@login_required
def analysis_chatbot(request):
    if request.method == 'POST':
        
        message_ = request.POST['message']
        print(message_)
        ai_response = indicator_chatbot(message_)
        print(ai_response)
        if ai_response:
        
            request.session['ai_response'] = ai_response
        else:
        
            messages.error(request, 'Please try again, the AI is out of service.')
        
        if 'ai_response' in request.session:    
            pass
        else:
            messages.error(request, 'Please ask your question')
            return redirect('home')

        context = {}
        context['message_'] = message_
        context['ai_response'] = request.session['ai_response']
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'indicator_chatbot.html', context)
        
@login_required
def economy_chatbot(request):
    if request.method == 'POST':
        
        message_ = request.POST['message']
        print(message_)
        ai_response = chatbot(message_)
        print(ai_response)
        if ai_response:
        
            request.session['ai_response'] = ai_response
        else:
        
            messages.error(request, 'Please try again, the AI is out of service.')
        
        if 'ai_response' in request.session:    
            pass
        else:
            messages.error(request, 'Please ask your question')
            return redirect('home')

        context = {}
        context['message_'] = message_
        context['ai_response'] = request.session['ai_response']
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'economy_chatbot.html', context)
        
@login_required       
def trading_chatbot(request):
    if request.method == 'POST':
        
        message_ = request.POST['message']
        print(message_)
        ai_response = chatbot(message_)
        print(ai_response)
        if ai_response:
        
            request.session['ai_response'] = ai_response
        else:
        
            messages.error(request, 'Please try again, the AI is out of service.')
        
        if 'ai_response' in request.session:    
            pass
        else:
            messages.error(request, 'Please ask your question')
            return redirect('home')

        context = {}
        context['message_'] = message_
        context['ai_response'] = request.session['ai_response']
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'trading_chatbot.html', context)


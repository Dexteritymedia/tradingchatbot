from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, View, FormView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .models import TradingBot
#from .utils import *
from .forms import SignUpForm
from .functions import *

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


def login_page(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}!!!")
            return redirect("home")
        else:
            messages.info(request, f"Account does not exist please sign up or check your account details")
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


class HomeTemplateView(TemplateView):
    template_name = "index.html"

@login_required(login_url="login")
def chatbot_page(request):
    #user = get_object_or_404(TradingBot, id=user_id)
    #check if user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            #get user input from the form
            user_input = request.POST['userInput']
            print(user_input)

            bot_response = indicator_chatbot_function(user_input)
            print(bot_response)

            message_history = TradingBot.objects.get_or_create(
                user=request.user,
                message=user_input,
                bot_response=bot_response,
            )
            return redirect(request.META['HTTP_REFERER'])
        else:
            #retrieve all messages belong to logged in user
            get_history = TradingBot.objects.filter(user=request.user).order_by('-id')
            context = {'get_history':get_history}
            return render(request, 'homepage.html', context)
    else:
        return redirect("login")


@login_required(login_url="login")
def delete_history(request):
    delete_all_msg = TradingBot.objects.filter(user = request.user)
    delete_all_msg.delete()
    return redirect(request.META['HTTP_REFERER'])

class TradingBotDeleteView(LoginRequiredMixin, DeleteView):
    # specify the model you want to use
    model = TradingBot
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"
     
    template_name = "delete_message.html"

    def form_valid(self, form):
        messages.success(self.request, 'This message has been deleted.')
        return super(TradingBotDeleteView, self).form_valid(form)


@login_required(login_url="login")
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
        return render(request, 'ai_response.html', context)
    return render(request, 'indicator_chatbot.html',)

@login_required(login_url="login")
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
        return render(request, 'ai_response.html', context)
    return render(request, 'economy_chatbot.html',)

@login_required(login_url="login")
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
        return render(request, 'ai_response.html', context)
    return render(request, 'trading_chatbot.html',)


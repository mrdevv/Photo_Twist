# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Album_na_Zdjecia.authController import SecuredUser
from django.core.urlresolvers import reverse_lazy
from .forms import UserFormRegister, UserFormLogin



class UserFormView(View):
    form_class = UserFormRegister
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('album:index')

        return render(request, self.template_name, {'form': form})


# class LoginForm(View):
#     form_class = UserFormLogin
#     template_name = 'login.html'
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#
#         username = form.data['username']
#         password = form.data['password']
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('album:index')
#         else:
#             return render(request, self.template_name, {'form': form})

class LoginForm(View):
    form_class = UserFormLogin
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('album:index')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})



class LogoutView(View):
    form_class = UserFormLogin

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


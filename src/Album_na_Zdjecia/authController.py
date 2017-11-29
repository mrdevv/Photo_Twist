from django.shortcuts import render, redirect


class SecuredUser(object):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(SecuredUser, self).get(self, request, *args, **kwargs)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(SecuredUser, self).post(self, request, *args, **kwargs)
        else:
            return redirect('login')

from django.shortcuts import redirect


def auth_franchise(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.franchise:
                return func(request, *args, **kwargs)
        return redirect("official:loginpage")

    return wrap


def auth_pickupboy(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.pickup_boy:
                return func(request, *args, **kwargs)
        return redirect("official:loginpage")

    return wrap


def auth_customer(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.customer:
                return func(request, *args, **kwargs)
        return redirect("user:login")

    return wrap

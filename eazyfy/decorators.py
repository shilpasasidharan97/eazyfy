from django.shortcuts import redirect


def auth_franchise(func):
    def wrap(request, *args, **kwargs):
        franchise_ex = request.user.franchise
        if franchise_ex is not None:
            return func(request, *args, **kwargs)
        return redirect("official:loginpage")

    return wrap


def auth_pickupboy(func):
    def wrap(request, *args, **kwargs):
        pickupboy_ex = request.user.pickup_boy
        if pickupboy_ex is not None:
            return func(request, *args, **kwargs)
        return redirect("official:loginpage")

    return wrap


def auth_customer(func):
    def wrap(request, *args, **kwargs):
        customer_ex = request.user.customer
        if customer_ex is not None:
            return func(request, *args, **kwargs)
        return redirect("user:login")

    return wrap

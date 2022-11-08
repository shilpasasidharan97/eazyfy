from django.shortcuts import redirect


def auth_franchise(func):
    def wrap(request, *args, **kwargs):
        franchise_ex = request.user.franchise
        print(franchise_ex)
        if franchise_ex == "None":
            return func(request, *args, **kwargs)
        else:
            return redirect("official:loginpage")
    return wrap


def auth_pickupboy(func):
    def wrap(request, *args, **kwargs):
        pickupboy_ex = request.user.pickup_boy
        if pickupboy_ex == "None":
            return func(request, *args, **kwargs)
        else:
            return redirect("official:loginpage")
    return wrap


def auth_customer(func):
    def wrap(request, *args, **kwargs):
        customer_ex = request.user.customer
        if customer_ex == "None":
            return func(request, *args, **kwargs)
        else:
            return redirect("official:loginpage")
    return wrap
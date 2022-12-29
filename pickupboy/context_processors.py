from official.models import User


def main_context(request):
    if request.session.exists(request.session.session_key):
        pickupBoy = request.user.pickup_boy
        if User.objects.filter(pickup_boy=pickupBoy).exists():
            pickupBoy = request.user.pickup_boy
            return {"domain": request.META["HTTP_HOST"], "pickUpBoy": pickupBoy}
        return {"domain": request.META["HTTP_HOST"]}
    else:
        return {"domain": request.META["HTTP_HOST"]}

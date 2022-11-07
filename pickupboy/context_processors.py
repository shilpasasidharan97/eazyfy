from official.models import *


def main_context(request):
    pickUpBoy = PickUpBoy.objects.get(id=request.user.pickup_boy.id)
    return {
        "domain": request.META["HTTP_HOST"],
        "pickUpBoy":pickUpBoy,
    }
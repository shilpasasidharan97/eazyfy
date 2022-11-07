from official.models import *


def main_context(request):
    brand = Brand.objects.all()
    user_object = request.user
   
    return {
        "domain": request.META["HTTP_HOST"],
        "brand":brand,
        "user_object" : user_object,
    }
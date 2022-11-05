from official.models import *


def main_context(request):
    brand = Brand.objects.all()
    return {
        "domain": request.META["HTTP_HOST"],
        "brand":brand,
    }
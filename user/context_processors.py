from official.models import Brand


def main_context(request):
    brand = Brand.objects.all()
    if request.session.exists(request.session.session_key):
        user_object = request.user
        return {"domain": request.META["HTTP_HOST"], "brand": brand, "status": 1, "user_object": user_object}
    return {"brand": brand, "domain": request.META["HTTP_HOST"], "status": 0}

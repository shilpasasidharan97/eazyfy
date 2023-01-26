from official.models import Brand,BrandModel


def main_context(request):
    brands = Brand.objects.all()
    most_selling_models = BrandModel.objects.filter(is_mostselling=True)
    if request.session.exists(request.session.session_key):
        user_object = request.user
        return {"domain": request.META["HTTP_HOST"], "brands": brands, "status": 1, "user_object": user_object, "most_selling_models":most_selling_models}
    return {"brands": brands, "domain": request.META["HTTP_HOST"], "status": 0, "most_selling_models":most_selling_models}

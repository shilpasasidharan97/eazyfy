from official.models import Brand, Customer
from official.models import BrandModel

from .models import City
from django.urls import reverse


def main_context(request):
    brands = Brand.objects.all()
    models = BrandModel.objects.all()
    most_selling_models = models.filter(is_mostselling=True)
    cities = City.objects.all()
    if request.user.is_authenticated and request.user.usertype == "customer":
        if not Customer.objects.filter(user=request.user).exists():
            Customer(user=request.user).save()

    status = 1 if request.session.exists(request.session.session_key) else 0
    search_suggestions = [
        {"name": model.name, "link": reverse("main:device_page", kwargs={"slug": model.slug})} for model in models
    ]
    context = {
        "domain": request.META["HTTP_HOST"],
        "cities": cities,
        "brands": brands,
        "models": models,
        "most_selling_models": most_selling_models,
        "status": status,
        "search_links": search_suggestions,
    }
    return context

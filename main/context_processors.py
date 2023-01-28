import json
from .models import City
from official.models import Brand
from official.models import BrandModel
from django.urls import reverse


def main_context(request):
    brands = Brand.objects.all()
    models = BrandModel.objects.all()
    most_selling_models = models.filter(is_mostselling=True)
    cities = City.objects.all()
    status = 1 if request.session.exists(request.session.session_key) else 0
    search_suggestions = [
        {"name": model.name, "link": reverse("user:device_page", kwargs={"slug": model.slug})} for model in models
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

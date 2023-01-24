from .models import City


def main_context(request):
    return {"cities": City.objects.all()}

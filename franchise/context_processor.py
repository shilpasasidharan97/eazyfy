from official.models import User


def main_context(request):
    if request.session.exists(request.session.session_key):
        franchise = request.user.franchise
        if User.objects.filter(franchise=franchise).exists():
            franchise = request.user.franchise
            return {"domain": request.META["HTTP_HOST"], "franchise": franchise}
        return {"domain": request.META["HTTP_HOST"]}
    return {"domain": request.META["HTTP_HOST"]}

from official.models import *

def main_context(request):
    if request.session.exists(request.session.session_key):
        franchise = request.user.franchise
        if User.objects.filter(franchise=franchise).exists():
            franchise = request.user.franchise
            # franchise_obj=Franchise.objects.get(name=franchise)
            return {
                "domain": request.META["HTTP_HOST"],
                "franchise":franchise,
                # 'franchise_obj':franchise_obj
            }
        else:
            return {
                "domain": request.META["HTTP_HOST"],
            }
    else:
        return {
            "domain": request.META["HTTP_HOST"],
        }



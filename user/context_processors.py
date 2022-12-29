from official.models import Brand


def main_context(request):
    brand = Brand.objects.all()
    # indexSearch = BrandModel.objects.filter(brand__id=id)
    # data = []
    # for pos in indexSearch:
    #     item = {
    #         "pk":pos.pk,
    #         "modelName":pos.name
    #     }
    #     data.append(item)

    if request.session.exists(request.session.session_key):
        user_object = request.user
        return {"domain": request.META["HTTP_HOST"], "brand": brand, "status": 1, "user_object": user_object}
    else:
        return {"brand": brand, "domain": request.META["HTTP_HOST"], "status": 0}


# def IndexSearch(request):
#     indexSearch = BrandModel.objects.filter(brand__id=id)
#     data = []
#     for pos in indexSearch:
#         item = {
#             "pk":pos.pk,
#             "modelName":pos.name
#         }
#         data.append(item)

#         return{
#             "domain": request.META["HTTP_HOST"],
#             "indexSearch" : indexSearch
#         }

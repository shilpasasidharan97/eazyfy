from django.urls import path
from . import views

app_name = 'pickupboy'

urlpatterns = [
    path('',views.index,name="index"),
    path('base',views.base,name="base"),
    path('total-order',views.total_order,name="total-order"),
    path('customer-selfy',views.customer_selfy,name="customer-selfy"),
    path('product-details',views.product_details,name="product-details"),
    path('verification-questions',views.verification_questions,name="verification-questions"),
    path('complete',views.complete,name="complete"),
    path('fail',views.fail,name="fail"),
    path('requote',views.requote,name="requote"),

    ]



    
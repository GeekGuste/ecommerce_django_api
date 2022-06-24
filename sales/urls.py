from django.urls import re_path
from sales import views

urlpatterns = [
    re_path(r'^create-payment/$', views.create_payment),
    re_path(r'^confirm-payment/$', views.confirm_payment),
    re_path(r'^save-paypal-order/$', views.save_paypal_order),
    re_path(r'^contact/$', views.contact),
]
from django.urls import path
from .views import SendPaymentInfoView, VerifyPaymentView

urlpatterns = [
    path("send_info_payment/", SendPaymentInfoView.as_view(), name="send_info_payment"),
    path("verify/", VerifyPaymentView.as_view(), name="verify_payment"),
]

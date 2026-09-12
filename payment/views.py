from django.shortcuts import render, redirect
from django.contrib import messages
from appointments.models import TimeSlot
from django.views.generic import View
from .service import SandBoxPayment, sand_box_urls
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TransActoin
from dotenv import load_dotenv
import os
from decimal import Decimal

load_dotenv()


class SendPaymentInfoView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        amount = request.POST.get("balance")

        payment = SandBoxPayment(sand_box_urls)

        description = "this is for get appointment"
        call_back_url = "http://127.0.0.1:8000/payment/verify/"
        metadata = {"email": user.email}
        status, data = payment.send_information(
            os.getenv("MERCHAT_ID", ""), amount, description, call_back_url, metadata
        )
        if status:
            try:
                authority = data["data"]["authority"]
                transaction = TransActoin(
                    user=user,
                    porpuse="Charge Wallet",
                    amount=amount,
                    authority=authority,
                )
                transaction.save()
                url = payment.redirect_to_zarinpal(data)
                return redirect(url)
            except Exception as e:
                print(f"{e}")
                messages.error(request, "پرداخت با خطا مواجه شد")
                return redirect("wallet")
        messages.error(request, "پرداخت با خطا مواجه شد")
        return redirect("wallet")


class VerifyPaymentView(LoginRequiredMixin, View):

    def get(self, request):
        authority = request.GET.get("Authority")
        status = request.GET.get("Status")
        if status == "OK":
            transaction = TransActoin.objects.get(authority=authority)
            user = transaction.user
            amount = transaction.amount
            merchat_id = os.getenv("MERCHAT_ID", "")
            data = {
                "merchant_id": merchat_id,
                "amount": amount,
                "authority": authority,
            }
            sandboxpayment = SandBoxPayment(sand_box_urls)
            status, data = sandboxpayment.verify(data)
            if status:

                if data["data"]["code"] == 100 or data["data"]["code"] == 101:
                    transaction.card_number = data["data"]["card_pan"]
                    transaction.fee = data["data"]["fee"]
                    transaction.save()
                    user_amount = user.wallet.balance
                    user.wallet.balance = user_amount + Decimal(amount)
                    user.wallet.save(update_fields=["balance"])
                    messages.success(request, "پرداخت با موفقیت انجام شد")
                    return redirect("wallet")
                else:
                    messages.error(request, "پرداخت با خطا مواجه شد")
                    return redirect("wallet")

            else:
                messages.error(request, "پرداخت با خطا مواجه شد")
                return redirect("wallet")
        else:
            messages.error(request, "پرداخت با خطا مواجه شد")
            return redirect("wallet")

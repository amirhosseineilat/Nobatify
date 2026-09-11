from .models import Otp
from django.contrib import messages
from django.utils.timezone import now
from utils.notifications import Sender
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountService:
    @staticmethod
    def request_password_reset(request, user_email, sender: Sender):
        try:
            user = User.objects.get(email=user_email)
            otp = Otp()
            otp_code = otp.generate_otp(user=user, purpose="password_reset")
            message = f"Your OTP code is: {otp_code}"
            sender.send_notification(user, message)
            print("OTP sent successfully to", user.email)
            messages.success(request, "کد به ایمیل شما ارسال شد")
            return True
        except User.DoesNotExist:
            print("User not found")
            messages.error(request, "یوزری با این ایمیل پیدا نشد")
            return False
        except Exception as e:
            messages.error(request, "ارسال با خطا مواجه شد دوباره امتحان کنید")
            print("Failed to send OTP:", str(e))
            return False

    def validate_otp(request, otp_code, purpose):
        try:
            otp: Otp = Otp.objects.get(
                code=otp_code, expire_time__gte=now(), is_used=False, purpose=purpose
            )
            otp.is_used = True
            otp.save()
            return True, otp.user
        except Otp.DoesNotExist:
            messages.error(request, "کد اشتباه است")
            return False, None

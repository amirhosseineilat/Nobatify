from .models import Otp
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.timezone import now
from utils.notifications import Sender


class AccountService:
    @staticmethod
    def request_password_reset(user_email, sender: Sender):
        try:
            user = User.objects.get(email=user_email)
            otp = Otp()
            otp_code = otp.generate_otp(user=user, purpose="password_reset")
            message = f"Your OTP code is: {otp_code}"
            sender.send_notification(user, message)
            print("OTP sent successfully to", user.email)

        except User.DoesNotExist:
            print("User not found")
            return
        except Exception as e:
            print("Failed to send OTP:", str(e))

    def validate_otp(otp_code, purpose):
        try:
            otp: Otp = Otp.objects.get(
                code=otp_code, expire_time__gte=now(), is_used=False, purpose=purpose
            )
            otp.is_used = True
            otp.save()
            return True, otp.user
        except Otp.DoesNotExist:
            return False, None

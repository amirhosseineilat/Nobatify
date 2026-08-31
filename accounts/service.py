from abc import ABC, abstractmethod
from .models import Otp
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os
from django.utils.timezone import now


class Notification(ABC):
    @abstractmethod
    def send(self, user: User, message: str):
        pass


class EmailNotification(Notification):
    def send(self, user: User, message: str):
        send_mail(
            subject="Nobatify OTP Notification",
            message=message,
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[user.email],
        )


class Sender:
    def __init__(self, notification: Notification):
        self._notification = notification

    def send_notification(self, user: User, message: str):
        self._notification.send(user, message)


class AccountService:
    @staticmethod
    def request_password_reset(user_email, sender: Sender):
        try:
            user = User.objects.get(email=user_email)
            otp_code = Otp.generate_otp(user=user, purpose="password_reset")
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

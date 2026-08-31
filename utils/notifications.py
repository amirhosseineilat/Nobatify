from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os


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

from .models import Doctor, Comment, Speciality
from appointments.models import Appointment
from django.db.models import Q
from utils.notifications import Sender
from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorService:

    @staticmethod
    def search(q):
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(specialities__name__icontains=q)
        ).distinct()
        return doctors

    @staticmethod
    def send_reserved_notification(
        user: User, provider_name: str, appointment: Appointment, sender: Sender
    ):
        message = f"""

Hello,

Your appointment has been successfully booked. ✅

**Appointment Details:**

* 👤 Name: { user.username }
* 🏥 Service Provider: { provider_name }
* 📅 Date: { appointment.date }
* 🕐 Time: { appointment.time }

Please make sure to arrive at the scheduled location on the specified date and time.

If you need to cancel or reschedule your appointment, you can do so through your account.

Thank you,
**The Nobatify Team**

    """
        sender.send_notification(user, message)

from .models import Doctor, Comment, Speciality
from django.contrib.auth.models import User
from appointments.models import Appointment
from django.db.models import Q
from utils.notifications import Sender


class DoctorService:

    @staticmethod
    def search(q):
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(speciality__name__icontains=q)
        ).distinct()
        return doctors

    def send_reserved_nofication(
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

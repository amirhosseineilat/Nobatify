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
        jalali_date = appointment.date.strftime("%Y/%m/%d")
        message = f"""

سلام،

نوبت شما با موفقیت رزرو شد. ✅

**جزئیات نوبت:**

* 👤 نام: {user.username}
* 🏥 آدرس مطب: {appointment.doctor.address}
* 📅 تاریخ: {jalali_date}
* 🕐 ساعت: {appointment.start_time}

لطفاً در تاریخ و ساعت مشخص‌شده در محل ارائه خدمات حضور داشته باشید.

در صورتی که نیاز به لغو یا تغییر زمان نوبت خود دارید، می‌توانید از طریق حساب کاربری خود اقدام کنید.

با تشکر،
**تیم Nobatify**

"""

        sender.send_notification(user, message)

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor, Comment, Speciality
from appointments.models import TimeSlot
from django.views.generic import DetailView, ListView, CreateView
from .service import DoctorService
from .forms import CommentForm, DoctorForm, SpecialityForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Avg, Count, Prefetch
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.


# base views
class BaseDetailDoctorView(DetailView):
    model = Doctor

    context_object_name = "doctor"

    def get_queryset(self):
        # return (
        #     Doctor.objects.prefetch_related("specialities")
        #     .annotate(
        #         avg_rating=Avg("comments__rating"),
        #         total_comments=Count("comments")
        #     )
        # )

        available_slots = TimeSlot.objects.filter(appointment__isnull=True)

        return Doctor.objects.prefetch_related(
            "specialities",
            Prefetch(
                "time_slots", queryset=available_slots, to_attr="available_time_slots"
            ),
        ).annotate(avg_rating=Avg("comments__rating"), total_comments=Count("comments"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object
        context["can_comment"] = doctor.has_patient(self.request.user)
        context["form"] = CommentForm()
        return context


class BaseListDoctorView(ListView):
    model = Doctor
    context_object_name = "doctors"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["specialities"] = Speciality.objects.all()

        return context

    def get_queryset(self):
        return Doctor.objects.annotate(
            avg_rating=Avg("comments__rating"), total_comments=Count("comments")
        )


class BaseCreateDoctorView(CreateView):
    model = Doctor
    form_class = DoctorForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BaseCreateSpecialityView(CreateView):
    model = Speciality
    form_class = SpecialityForm


# public view
class DoctorDetailView(BaseDetailDoctorView):
    template_name = "doctors/doctor_detail.html"


class DoctorListView(BaseListDoctorView):
    template_name = "doctors/doctor_list.html"


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=self.kwargs.get("doctor_id"))
        
        
        if not doctor.has_patient(request.user):
            messages.error(request, "تنها بیمارانی که با این پزشک نوبت داشته‌اند می‌توانند نظر ثبت کنند.")
            return redirect("doctor_detail", pk=doctor.pk)
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        doctor_id = self.kwargs.get("doctor_id")
        form.instance.doctor = get_object_or_404(Doctor, pk=doctor_id)
        messages.success(self.request, "نظر شما با موفقیت ثبت شد.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("doctor_detail", kwargs={"pk": self.kwargs.get("doctor_id")})
class BaseSearchDoctorView(BaseListDoctorView):
    context_object_name = "doctors"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     context["specialities"] = Speciality.objects.all()

    #     return context

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if q:
            return DoctorService.search(q)
        return Doctor.objects.all()


class SearchDoctorView(BaseSearchDoctorView):
    pass


class FilterDoctorView(BaseSearchDoctorView):

    def get_queryset(self):

        speciality = self.request.GET.get("speciality", "").strip()
        avg_rate = self.request.GET.get("avg_rate", "").strip()

        if speciality or avg_rate:
            return DoctorService.filter(avg_rate, speciality)

        return Doctor.objects.all()

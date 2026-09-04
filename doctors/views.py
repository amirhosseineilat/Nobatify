from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor, Comment,Speciality
from appointments.models import TimeSlot
from django.views.generic import DetailView, ListView, CreateView
from .service import DoctorService
from .forms import CommentForm,DoctorForm,SpecialityForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Avg, Count, Prefetch


# Create your views here.

#base views
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

        available_slots = TimeSlot.objects.filter(
            appointment__isnull=True
        )

        return Doctor.objects.prefetch_related(
            "specialities",
            Prefetch(
                "time_slots",
                queryset=available_slots,
                to_attr="available_time_slots"
            )
        ).annotate(
            avg_rating=Avg("comments__rating"),
            total_comments=Count("comments")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
class BaseListDoctorView(ListView):
    model = Doctor
    context_object_name = "doctors"

    def get_queryset(self):
        return Doctor.objects.annotate(
            avg_rating=Avg('comments__rating'),
            total_comments=Count('comments')
        )
class BaseCreateDoctorView(CreateView):
    model = Doctor
    form_class = DoctorForm
class BaseCreateSpecialityView(CreateView):
    model = Speciality
    form_class = SpecialityForm

#public view
class DoctorDetailView(BaseDetailDoctorView):
    template_name = "doctors/doctor_detail.html"
        
class DoctorListView(BaseListDoctorView):
    template_name = "doctors/doctor_list.html"
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    http_method_names = ['post']
    def form_valid(self, form):
        form.instance.user = self.request.user
        doctor_id = self.kwargs.get('doctor_id')
        form.instance.doctor = get_object_or_404(Doctor, pk=doctor_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('doctor_detail', kwargs={'pk': self.kwargs.get('doctor_id')})

class SearchDoctorView(ListView):
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if q:
            return DoctorService.search(q)
        return Doctor.objects.all()

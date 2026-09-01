from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor, Comment
from django.views.generic import DetailView, ListView, CreateView
from .service import DoctorService
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Avg, Count
# Create your views here.


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctors/doctor_detail.html"
    context_object_name = "doctor"
    
    def get_queryset(self):
        return (
            Doctor.objects.prefetch_related("specialities")
            .annotate(
                avg_rating=Avg("comments__rating"),
                total_comments=Count("comments")
            ))


class DoctorListView(ListView):
    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"
    
    def get_queryset(self):
        return Doctor.objects.annotate(
            average_rating=Avg('comments__rating'),
            comment_count=Count('comments')
        )

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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import SiteContentForm
from .models import (
    AboutDetail,
    AboutStat,
    ContactMessage,
    CounterStat,
    PortfolioCategory,
    PortfolioItem,
    ResumeCertification,
    ResumeEducation,
    ResumeExperience,
    ServiceItem,
    SiteContent,
    SkillCategory,
    SocialLink,
    Testimonial,
)


def get_site_content():
    content, _ = SiteContent.objects.get_or_create(pk=1)
    return content


def index(request):
    content = get_site_content()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, "Message sent successfully.")
            return redirect(f"{reverse('index')}#contact")

        messages.error(request, "Please fill in all contact form fields.")

    context = {
        "content": content,
        "header_social_links": SocialLink.objects.filter(section="header", is_active=True),
        "hero_social_links": SocialLink.objects.filter(section="hero", is_active=True),
        "about_stats": AboutStat.objects.filter(is_active=True),
        "about_details": AboutDetail.objects.filter(is_active=True),
        "counter_stats": CounterStat.objects.filter(is_active=True),
        "skill_categories": SkillCategory.objects.filter(is_active=True).prefetch_related("skills"),
        "resume_experiences": ResumeExperience.objects.filter(is_active=True).prefetch_related("points"),
        "resume_educations": ResumeEducation.objects.filter(is_active=True),
        "resume_certifications": ResumeCertification.objects.filter(is_active=True),
        "portfolio_categories": PortfolioCategory.objects.filter(is_active=True),
        "portfolio_items": PortfolioItem.objects.filter(is_active=True).select_related("category"),
        "service_items": ServiceItem.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
    }
    return render(request, "index.html", context)


@login_required
def admin_page(request):
    content = get_site_content()

    if request.method == "POST" and request.POST.get("action") == "save_content":
        form = SiteContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Frontend content updated.")
            return redirect("portfolio_admin")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = SiteContentForm(instance=content)

    all_messages = ContactMessage.objects.order_by("-created_at")
    today = timezone.localdate()
    context = {
        "content_form": form,
        "contact_messages": all_messages,
        "message_count": all_messages.count(),
        "today_message_count": all_messages.filter(created_at__date=today).count(),
    }
    return render(request, "admin.html", context)


@login_required
def delete_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(ContactMessage, pk=message_id)
        message.delete()
        messages.success(request, "Message deleted.")
    return redirect("portfolio_admin")


@login_required
def mark_message_read(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(ContactMessage, pk=message_id)
        message.is_read = True
        message.save(update_fields=["is_read"])
    return redirect("portfolio_admin")

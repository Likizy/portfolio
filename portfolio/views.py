from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ContactMessageForm, SiteContentForm
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


CONTENT_FORM_SECTIONS = (
    (
        "Brand & hero",
        "Your site name, introduction, imagery, and primary calls to action.",
        (
            "site_name",
            "hero_name",
            "hero_roles",
            "hero_description",
            "hero_image",
            "hero_primary_button_label",
            "hero_primary_button_link",
            "hero_secondary_button_label",
            "hero_secondary_button_link",
        ),
    ),
    (
        "About",
        "The personal information and calls to action shown in the About section.",
        (
            "about_badge",
            "about_title",
            "about_description_1",
            "about_description_2",
            "about_name",
            "about_profession",
            "about_email",
            "about_phone",
            "about_location",
            "about_image",
            "about_resume_label",
            "about_resume_link",
            "about_talk_label",
            "about_talk_link",
        ),
    ),
    (
        "Resume",
        "The resume title, summary, profile image, and contact information.",
        (
            "resume_title",
            "resume_summary",
            "resume_profile_image",
            "resume_location",
            "resume_email",
            "resume_phone",
        ),
    ),
    (
        "Portfolio & services",
        "Headlines, introductions, and the main services call to action.",
        (
            "portfolio_title",
            "portfolio_intro",
            "services_title",
            "services_intro",
            "services_heading_line_1",
            "services_heading_line_2",
            "services_summary",
            "services_button_label",
            "services_button_link",
        ),
    ),
    (
        "Testimonials & contact",
        "Section introductions and the details visitors use to reach you.",
        (
            "testimonials_title",
            "testimonials_intro",
            "contact_title",
            "contact_section_intro",
            "contact_intro",
            "contact_location",
            "contact_phone",
            "contact_email",
            "contact_form_title",
            "contact_form_intro",
        ),
    ),
    (
        "Footer",
        "The brand and copyright text shown at the bottom of the site.",
        ("footer_brand", "footer_text"),
    ),
)


def get_content_form_sections(form):
    return [
        {
            "title": title,
            "description": description,
            "fields": [form[field_name] for field_name in field_names],
        }
        for title, description, field_names in CONTENT_FORM_SECTIONS
    ]


def get_site_content():
    content, _ = SiteContent.objects.get_or_create(pk=1)
    return content


def index(request):
    content = get_site_content()

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Message sent successfully.")
            return redirect(f"{reverse('index')}#contact")

        messages.error(request, "Please provide a valid name, email, subject, and message.")

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
        "content_form_sections": get_content_form_sections(form),
        "contact_messages": all_messages,
        "message_count": all_messages.count(),
        "today_message_count": all_messages.filter(created_at__date=today).count(),
        "unread_message_count": all_messages.filter(is_read=False).count(),
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

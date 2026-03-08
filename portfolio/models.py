from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteContent(models.Model):
    site_name = models.CharField(max_length=100, default="KizTech")

    hero_name = models.CharField(max_length=120, default="Caleb Ezekiel Hatbwan")
    hero_roles = models.CharField(
        max_length=255,
        default="UI/UX Designer, Web Developer, Data Analyst, Mobile Developer",
        help_text="Comma-separated roles shown in the hero section.",
    )
    hero_description = models.TextField(
        default=(
            "Passionate about creating exceptional digital experiences that blend "
            "innovative design with functional development. Let's bring your vision to life."
        )
    )
    hero_image = models.FileField(upload_to="site/", blank=True, null=True)
    hero_primary_button_label = models.CharField(max_length=60, default="View My Work")
    hero_primary_button_link = models.CharField(max_length=120, default="#portfolio")
    hero_secondary_button_label = models.CharField(max_length=60, default="Get In Touch")
    hero_secondary_button_link = models.CharField(max_length=120, default="#contact")

    about_badge = models.CharField(max_length=120, default="Get to Know Me")
    about_title = models.CharField(max_length=255, default="Passionate About Creating Digital Experiences")
    about_description_1 = models.TextField(blank=True, default="")
    about_description_2 = models.TextField(blank=True, default="")
    about_name = models.CharField(max_length=120, default="Caleb Ezekiel Hatbwan")
    about_profession = models.CharField(max_length=120, default="Software Developer")
    about_email = models.EmailField(default="calebezekielhatbwan@gmail.com")
    about_phone = models.CharField(max_length=50, default="+234 0812 866 6531")
    about_location = models.CharField(max_length=255, default="Lagos, Nigeria")
    about_image = models.FileField(upload_to="site/", blank=True, null=True)
    about_resume_label = models.CharField(max_length=60, default="Download Resume")
    about_resume_link = models.CharField(max_length=255, default="#")
    about_talk_label = models.CharField(max_length=60, default="Let's Talk")
    about_talk_link = models.CharField(max_length=255, default="#contact")

    resume_title = models.CharField(max_length=120, default="Resume")
    resume_summary = models.TextField(blank=True, default="")
    resume_profile_image = models.FileField(upload_to="site/", blank=True, null=True)
    resume_location = models.CharField(max_length=255, default="Lagos Nigeria")
    resume_email = models.EmailField(default="calebezekielhatbwan@gmail.com")
    resume_phone = models.CharField(max_length=50, default="+234 0812 866 6531")

    portfolio_title = models.CharField(max_length=120, default="Portfolio")
    portfolio_intro = models.TextField(blank=True, default="")

    services_title = models.CharField(max_length=120, default="Services")
    services_intro = models.TextField(blank=True, default="")
    services_heading_line_1 = models.CharField(max_length=120, default="Innovative business")
    services_heading_line_2 = models.CharField(max_length=120, default="performance solutions")
    services_summary = models.TextField(blank=True, default="")
    services_button_label = models.CharField(max_length=60, default="View All Services")
    services_button_link = models.CharField(max_length=255, default="#services")

    testimonials_title = models.CharField(max_length=120, default="Testimonials")
    testimonials_intro = models.TextField(blank=True, default="")

    contact_title = models.CharField(max_length=120, default="Contact")
    contact_section_intro = models.TextField(blank=True, default="")
    contact_intro = models.TextField(
        default="Reach out for projects, collaborations, and business inquiries."
    )
    contact_location = models.CharField(max_length=255, default="Lagos, Nigeria")
    contact_phone = models.CharField(max_length=50, default="+234 0812 866 6531")
    contact_email = models.EmailField(default="calebezekielhatbwan@gmail.com")
    contact_form_title = models.CharField(max_length=120, default="Get In Touch")
    contact_form_intro = models.TextField(blank=True, default="")

    footer_brand = models.CharField(max_length=120, default="iPortfolio")
    footer_text = models.CharField(max_length=255, default="All Rights Reserved")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Content"


class SocialLink(models.Model):
    SECTION_CHOICES = (
        ("header", "Header"),
        ("hero", "Hero"),
    )

    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default="header")
    platform = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=80, default="bi bi-link-45deg")
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.get_section_display()}: {self.platform}"


class AboutStat(models.Model):
    value = models.CharField(max_length=20)
    label = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"


class AboutDetail(models.Model):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class CounterStat(models.Model):
    icon_class = models.CharField(max_length=80, default="bi bi-emoji-smile")
    value = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class SkillCategory(models.Model):
    title = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Skill categories"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=120)
    percentage = models.PositiveIntegerField(default=50)
    tooltip = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title} ({self.percentage}%)"


class ResumeExperience(models.Model):
    title = models.CharField(max_length=120)
    period = models.CharField(max_length=80)
    company = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ResumeExperiencePoint(models.Model):
    experience = models.ForeignKey(
        ResumeExperience,
        on_delete=models.CASCADE,
        related_name="points",
    )
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class ResumeEducation(models.Model):
    title = models.CharField(max_length=120)
    period = models.CharField(max_length=80)
    school = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ResumeCertification(models.Model):
    title = models.CharField(max_length=150)
    year = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Portfolio categories"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    title = models.CharField(max_length=120)
    image = models.FileField(upload_to="portfolio/")
    details_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ServiceItem(models.Model):
    title = models.CharField(max_length=120)
    highlighted_word = models.CharField(max_length=80, blank=True)
    description = models.TextField()
    icon_class = models.CharField(max_length=80, default="bi bi-gear")
    link = models.CharField(max_length=255, default="#")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    quote = models.TextField()
    image = models.FileField(upload_to="testimonials/", blank=True, null=True)
    highlight = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

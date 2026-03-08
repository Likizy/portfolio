from django.contrib import admin

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
    ResumeExperiencePoint,
    ServiceItem,
    SiteContent,
    Skill,
    SkillCategory,
    SocialLink,
    Testimonial,
)


class ResumeExperiencePointInline(admin.TabularInline):
    model = ResumeExperiencePoint
    extra = 1


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("site_name", "hero_name", "updated_at")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "section", "url", "order", "is_active")
    list_filter = ("section", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("platform", "url")


@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(AboutDetail)
class AboutDetailAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(CounterStat)
class CounterStatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "percentage", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ResumeExperience)
class ResumeExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "period", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [ResumeExperiencePointInline]


@admin.register(ResumeEducation)
class ResumeEducationAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "period", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ResumeCertification)
class ResumeCertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "highlighted_word", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "highlight", "order", "is_active")
    list_filter = ("highlight", "is_active")
    list_editable = ("highlight", "order", "is_active")

from django import forms

from .models import SiteContent


class ContactMessageForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField()


class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        fields = [
            "site_name",
            "hero_name",
            "hero_roles",
            "hero_description",
            "hero_image",
            "hero_primary_button_label",
            "hero_primary_button_link",
            "hero_secondary_button_label",
            "hero_secondary_button_link",
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
            "resume_title",
            "resume_summary",
            "resume_profile_image",
            "resume_location",
            "resume_email",
            "resume_phone",
            "portfolio_title",
            "portfolio_intro",
            "services_title",
            "services_intro",
            "services_heading_line_1",
            "services_heading_line_2",
            "services_summary",
            "services_button_label",
            "services_button_link",
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
            "footer_brand",
            "footer_text",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.URLInput)):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "form-control", "rows": 3})
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({"class": "form-control"})

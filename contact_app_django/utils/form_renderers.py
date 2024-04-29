from django.forms.renderers import TemplatesSetting


class HtmxFormRenderer(TemplatesSetting):
    form_template_name = "htmx_form.html"


class HtmxFormMixin:
    default_renderer = HtmxFormRenderer()

    # def __init__(self, *args, **kwargs) -> None:
    #     return super().__init__(*args, label_suffix="", **kwargs)

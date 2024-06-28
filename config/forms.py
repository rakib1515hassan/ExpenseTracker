from django.forms.renderers import BaseRenderer
from django.template.loader import get_template


class CustomDivFormRenderer(BaseRenderer):
    form_template_name = "utils/form_snippet.html"

    def get_template(self, template_name):
        return get_template(template_name)

    def render(self, template_name, context, request=None, renderer=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()

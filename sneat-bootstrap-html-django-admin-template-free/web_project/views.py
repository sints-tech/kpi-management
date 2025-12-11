from django.views.generic import TemplateView
from django.http import HttpResponse
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


class SystemView(TemplateView):
    template_name = "pages/system/not-found.html"
    status = ""
    status_code = 200

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Define the layout for this module
        # _templates/layout/system.html
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("system.html", context),
                "status": self.status,
            }
        )

        return context

    def render_to_response(self, context, **response_kwargs):
        # Set status code from the view instance
        response_kwargs.setdefault('status', self.status_code)
        return super().render_to_response(context, **response_kwargs)

    @classmethod
    def as_view(cls, **initkwargs):
        # Extract status code from initkwargs and set it as an instance attribute
        status_code = initkwargs.pop('status', 200)
        view = super().as_view(**initkwargs)

        def wrapped_view(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            if hasattr(response, 'status_code'):
                response.status_code = status_code
            return response

        return wrapped_view

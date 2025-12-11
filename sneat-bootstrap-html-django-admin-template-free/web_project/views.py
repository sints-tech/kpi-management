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
        import logging
        logger = logging.getLogger(__name__)
        
        # Log untuk debugging - jika method ini dipanggil, berarti request masuk ke handler 404
        logger.warning(f"SystemView.get_context_data called for path: {self.request.path if hasattr(self, 'request') else 'unknown'}")
        
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            logger.error(f"Error in super().get_context_data: {e}", exc_info=True)
            context = {}
        
        try:
            context = TemplateLayout.init(self, context)
        except Exception as e:
            logger.error(f"Error in TemplateLayout.init: {e}", exc_info=True)
            if 'layout_path' not in context:
                context['layout_path'] = 'layout/system.html'

        # Define the layout for this module
        # _templates/layout/system.html
        try:
            layout_path = TemplateHelper.set_layout("system.html", context)
            context.update({
                "layout_path": layout_path,
                "status": self.status,
            })
        except Exception as e:
            logger.error(f"Error in TemplateHelper.set_layout: {e}", exc_info=True)
            context.update({
                "layout_path": "layout/system.html",
                "status": self.status,
            })

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

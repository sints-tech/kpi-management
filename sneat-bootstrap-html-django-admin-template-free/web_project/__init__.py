
# from web_project.bootstrap import TemplateBootstrap
from web_project.template_helpers.theme import TemplateHelper
from django.conf import settings


class TemplateLayout:
    # Initialize the bootstrap files and page layout
    @staticmethod
    def init(view_or_request, context):
        # Init the Template Context using TEMPLATE_CONFIG
        # view_or_request can be either a view instance or request object (for function-based views)

        # Set a default layout globally using settings.py. Can be set in the page level view file as well.
        layout = "vertical"

        # Set the selected layout dengan error handling
        try:
            layout_path = TemplateHelper.set_layout(
                "layout_" + layout + ".html", context
            )
            context.update({"layout_path": layout_path})
        except Exception as e:
            # Fallback jika set_layout gagal
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"TemplateHelper.set_layout failed: {e}")
            context['layout_path'] = 'layout/layout_vertical.html'

        # Map context variables dengan error handling
        try:
            TemplateHelper.map_context(context)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"TemplateHelper.map_context failed: {e}")

        return context

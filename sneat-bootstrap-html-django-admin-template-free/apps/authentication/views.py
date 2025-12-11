from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # Initialize basic context first dengan error handling
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in super().get_context_data: {e}", exc_info=True)
            context = {}
        
        # A function to init the global layout. It is defined in web_project/__init__.py file
        try:
            context = TemplateLayout.init(self, context)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"TemplateLayout.init failed: {e}")
            if 'layout_path' not in context:
                context['layout_path'] = 'layout/layout_blank.html'

        # Update the context
        try:
            layout_path = TemplateHelper.set_layout("layout_blank.html", context)
            context.update({"layout_path": layout_path})
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"TemplateHelper.set_layout failed: {e}")
            if 'layout_path' not in context:
                context['layout_path'] = 'layout/layout_blank.html'

        return context
    
    def post(self, request, *args, **kwargs):
        """Handle login form submission"""
        email_username = request.POST.get('email-username', '')
        password = request.POST.get('password', '')
        
        if email_username and password:
            # Try to authenticate with username or email
            user = authenticate(request, username=email_username, password=password)
            if user is None:
                # Try with email if username fails
                try:
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=email_username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login berhasil!')
                return redirect('index')
            else:
                messages.error(request, 'Username/Email atau password salah!')
        
        return self.get(request, *args, **kwargs)

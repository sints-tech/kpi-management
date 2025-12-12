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
        # Log to ensure view is being called
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"AuthView.get_context_data called for path: {self.request.path}")
        
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context
    
    def post(self, request, *args, **kwargs):
        """Handle login form submission"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"AuthView.post called for path: {request.path}")
        
        email_username = request.POST.get('email-username', '')
        password = request.POST.get('password', '')
        
        logger.info(f"Login attempt - email_username: {email_username[:3]}***, password length: {len(password)}")
        
        if email_username and password:
            # Try to authenticate with username or email
            user = authenticate(request, username=email_username, password=password)
            if user is None:
                # Try with email if username fails
                try:
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=email_username)
                    user = authenticate(request, username=user_obj.username, password=password)
                    logger.info(f"Tried authentication with email, found user: {user_obj.username if user_obj else 'None'}")
                except User.DoesNotExist:
                    logger.warning(f"User with email {email_username} not found")
                    pass
            
            if user is not None:
                login(request, user)
                logger.info(f"Login successful for user: {user.username}")
                messages.success(request, 'Login berhasil!')
                return redirect('index')
            else:
                logger.warning(f"Login failed - invalid credentials for: {email_username[:3]}***")
                messages.error(request, 'Username/Email atau password salah!')
        else:
            logger.warning("Login attempt with empty email_username or password")
            messages.error(request, 'Email/Username dan password harus diisi!')
        
        return self.get(request, *args, **kwargs)

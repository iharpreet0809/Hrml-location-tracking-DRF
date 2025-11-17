"""
Custom middleware for HRMS Location Tracking System
"""
from django.shortcuts import redirect
from django.contrib import messages


class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control:
    - Superusers (admin): Only admin panel access
    - Regular employees: Only application pages (track, history)
    
    This ensures proper separation of concerns:
    - Admins manage data through Django admin
    - Employees use the application interface
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip middleware for static files, media, and API endpoints
        if (request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path.startswith('/api/')):
            return self.get_response(request)
        
        # Skip for login/logout pages and root
        if request.path in ['/', '/login/', '/logout/', '/admin/login/', '/admin/logout/']:
            return self.get_response(request)
        
        # If user is authenticated
        if request.user.is_authenticated:
            # Superuser trying to access application pages (except login)
            if request.user.is_superuser and not request.path.startswith('/admin/'):
                # Don't redirect if it's a POST to login (to avoid CSRF issues)
                if request.method == 'POST' and request.path == '/login/':
                    return self.get_response(request)
                    
                messages.warning(
                    request, 
                    'You are logged in as admin. Please use the admin panel or logout first.'
                )
                return redirect('/admin/')
            
            # Regular employee trying to access admin panel
            if not request.user.is_superuser and request.path.startswith('/admin/'):
                messages.error(
                    request,
                    'You do not have permission to access the admin panel. Please use the application.'
                )
                return redirect('/')
        
        response = self.get_response(request)
        return response

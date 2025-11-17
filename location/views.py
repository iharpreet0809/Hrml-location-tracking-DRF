from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Location
from .serializers import LocationSerializer
from .permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger('location')


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing location records.
    Provides list, create, retrieve, update, and delete operations.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """
        Filter queryset to return only the authenticated user's locations.
        Supports filtering by employee_id query parameter.
        """
        try:
            queryset = Location.objects.filter(employee=self.request.user)
            
            # Support filtering by employee_id (only if it matches the authenticated user)
            employee_id = self.request.query_params.get('employee_id', None)
            if employee_id is not None:
                try:
                    emp_id = int(employee_id)
                    # Security check: only allow filtering by own employee ID
                    if emp_id == self.request.user.id:
                        queryset = queryset.filter(employee_id=emp_id)
                    else:
                        logger.warning(
                            f"User {self.request.user.id} attempted to access "
                            f"locations for employee {emp_id}"
                        )
                except ValueError:
                    logger.warning(f"Invalid employee_id parameter: {employee_id}")
            
            return queryset
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}", exc_info=True)
            return Location.objects.none()
    
    def perform_create(self, serializer):
        """
        Set the employee to the authenticated user when creating a location.
        Prevents employee_id spoofing.
        """
        try:
            # Always use the authenticated user as the employee
            serializer.save(employee=self.request.user)
            logger.info(
                f"Location created for user {self.request.user.username} "
                f"(ID: {self.request.user.id})"
            )
        except Exception as e:
            logger.error(
                f"Error creating location for user {self.request.user.id}: {str(e)}",
                exc_info=True
            )
            raise
    
    def create(self, request, *args, **kwargs):
        """
        Override create to add additional security checks and better error handling.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except ValidationError as e:
            logger.warning(f"Validation error in create: {str(e)}")
            return Response(
                {'error': 'Invalid data provided', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            logger.warning(
                f"Permission denied for user {request.user.id}: {str(e)}"
            )
            return Response(
                {'error': 'You do not have permission to perform this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            logger.error(f"Unexpected error in create: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while processing your request'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to add error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except ObjectDoesNotExist:
            logger.warning(
                f"User {request.user.id} attempted to access non-existent location"
            )
            return Response(
                {'error': 'Location not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied:
            logger.warning(
                f"User {request.user.id} attempted to access unauthorized location"
            )
            return Response(
                {'error': 'You do not have permission to access this location'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            logger.error(f"Error in retrieve: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while retrieving the location'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request, *args, **kwargs):
        """
        Override list to add error handling.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in list: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while retrieving locations'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def employee_login_view(request):
    """
    Custom login view for employees.
    """
    # If already logged in, redirect based on user type
    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.warning(request, 'You are logged in as admin. Please logout from admin panel first.')
            return redirect('/admin/')
        return redirect('/track/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a superuser
            if user.is_superuser:
                messages.error(request, 'Superusers should use the admin panel at /admin/')
                return render(request, 'login.html')
            
            # Login the employee
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to track page
            next_url = request.GET.get('next', '/track/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def employee_logout_view(request):
    """
    Logout view for employees.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('employee_login')


@login_required
def track_location_view(request):
    """
    View for the track location page.
    Only accessible by regular employees (non-superusers).
    """
    # Redirect superusers to admin panel
    if request.user.is_superuser:
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.warning(request, 'Superusers should use the admin panel to manage the system.')
        return redirect('/admin/')
    
    return render(request, 'track_location.html')


@login_required
def location_history_view(request):
    """
    View for the location history page.
    Only accessible by regular employees (non-superusers).
    """
    # Redirect superusers to admin panel
    if request.user.is_superuser:
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.warning(request, 'Superusers should use the admin panel to view all data.')
        return redirect('/admin/')
    
    return render(request, 'location_history.html')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_info_view(request):
    """
    API endpoint to get current employee information.
    Returns employee ID, username, and location count.
    
    GET /api/employee/
    """
    try:
        user = request.user
        location_count = Location.objects.filter(employee=user).count()
        
        data = {
            'employee_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'location_count': location_count,
            'is_active': user.is_active,
        }
        
        logger.info(f"Employee info retrieved for user {user.id}")
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving employee info: {str(e)}", exc_info=True)
        return Response(
            {'error': 'An error occurred while retrieving employee information'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    """
    API endpoint to get list of all employees with location tracking.
    Only returns employees who have tracked locations.
    
    GET /api/employees/
    """
    try:
        # Get all employees who have location records
        employees = User.objects.filter(locations__isnull=False).distinct()
        
        data = []
        for emp in employees:
            location_count = Location.objects.filter(employee=emp).count()
            latest_location = Location.objects.filter(employee=emp).first()
            
            data.append({
                'employee_id': emp.id,
                'username': emp.username,
                'email': emp.email,
                'location_count': location_count,
                'latest_location': {
                    'latitude': str(latest_location.latitude) if latest_location else None,
                    'longitude': str(latest_location.longitude) if latest_location else None,
                    'accuracy': str(latest_location.accuracy) if latest_location else None,
                    'timestamp': latest_location.timestamp if latest_location else None,
                } if latest_location else None
            })
        
        logger.info(f"Employee list retrieved: {len(data)} employees")
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving employee list: {str(e)}", exc_info=True)
        return Response(
            {'error': 'An error occurred while retrieving employee list'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

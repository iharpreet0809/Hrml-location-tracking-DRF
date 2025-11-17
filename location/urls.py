from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LocationViewSet, 
    track_location_view, 
    location_history_view,
    employee_info_view,
    employee_list_view,
    employee_login_view,
    employee_logout_view
)

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')

# Router automatically creates these URL patterns:
# GET    /api/locations/          -> list all locations (LocationViewSet.list)
# POST   /api/locations/          -> create new location (LocationViewSet.create)
# GET    /api/locations/{id}/     -> get specific location (LocationViewSet.retrieve)
# PUT    /api/locations/{id}/     -> update location (LocationViewSet.update)
# PATCH  /api/locations/{id}/     -> partial update (LocationViewSet.partial_update)
# DELETE /api/locations/{id}/     -> delete location (LocationViewSet.destroy)

urlpatterns = [
    # ==================== Authentication ====================
    path('', employee_login_view, name='employee_login'),
    path('login/', employee_login_view, name='employee_login'),
    path('logout/', employee_logout_view, name='employee_logout'),
    
    # ==================== API Endpoints ====================
    # Router URLs (see comments above for auto-generated endpoints)
    path('api/', include(router.urls)),
    
    # Custom API endpoints
    path('api/employee/', employee_info_view, name='employee_info'),      # GET - Current logged-in employee detail
    path('api/employees/', employee_list_view, name='employee_list'),     # GET - All employees list
    
    # ==================== Application Pages ====================
    path('history/', location_history_view, name='location_history'),     # Employee's own location history
    path('track/', track_location_view, name='track_location'),           # Track location page
]

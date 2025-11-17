# Design Document - Location Tracking Module

## Overview

The Location Tracking Module is a Django-based application that enables employees to track their GPS location and view their location history. The system follows a standard Django REST Framework architecture with ModelViewSet and routers, providing RESTful API endpoints for location management. The frontend consists of simple HTML/JavaScript pages that interact with the API using the browser's Geolocation API for GPS access.

### Technology Stack

- **Backend**: Django 4.x with Django REST Framework (DRF)
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: HTML5, JavaScript (Vanilla JS), CSS
- **Authentication**: Django's built-in authentication with DRF Token Authentication
- **API Pattern**: ModelViewSet with DefaultRouter

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend Layer                       │
│  ┌──────────────────────┐  ┌──────────────────────────┐│
│  │  Track Location Page │  │  Location History Page   ││
│  │  (HTML/JS)           │  │  (HTML/JS)               ││
│  └──────────────────────┘  └──────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ (HTTP/REST API)
┌─────────────────────────────────────────────────────────┐
│                      API Layer (DRF)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │         LocationViewSet (ModelViewSet)           │  │
│  │  - list()    - create()    - retrieve()          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Custom Permissions & Validators          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Business Logic Layer                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Serializers                         │  │
│  │  - LocationSerializer (validation)               │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     Data Layer (ORM)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Location Model                      │  │
│  │  - employee_id, lat, long, accuracy, timestamp   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Database (SQLite/PostgreSQL)          │
└─────────────────────────────────────────────────────────┘
```

### Application Structure

```
location_tracking/
├── hrms_project/              # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── location/                  # Django app
│   ├── models.py             # Location model
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets
│   ├── permissions.py        # Custom permissions
│   ├── urls.py               # API routing
│   └── management/
│       └── commands/
│           └── populate_locations.py  # Sample data
├── templates/                 # HTML templates
│   ├── track_location.html
│   └── location_history.html
├── static/                    # Static files
│   ├── css/
│   └── js/
└── manage.py
```

## Components and Interfaces

### 1. Data Model

**Location Model** (`location/models.py`)

```python
class Location(models.Model):
    employee = ForeignKey(User)           # Links to Django User model
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    accuracy = DecimalField(max_digits=10, decimal_places=2)
    timestamp = DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            Index(fields=['employee', '-timestamp']),
            Index(fields=['timestamp'])
        ]
```

**Field Specifications:**
- `employee`: Foreign key to Django's User model (represents employee_id)
- `latitude`: Decimal field with 6 decimal places (±90.000000)
- `longitude`: Decimal field with 6 decimal places (±180.000000)
- `accuracy`: Decimal field for GPS accuracy in meters
- `timestamp`: Auto-generated timestamp on record creation

### 2. API Layer

**LocationSerializer** (`location/serializers.py`)

```python
class LocationSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'employee_id', 'employee_name', 'latitude', 
                  'longitude', 'accuracy', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'employee_name']
    
    def validate_latitude(self, value):
        # Validate -90 to 90 range
    
    def validate_longitude(self, value):
        # Validate -180 to 180 range
    
    def validate_accuracy(self, value):
        # Validate positive number
```

**LocationViewSet** (`location/views.py`)

```python
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Filter by authenticated user
        # Support query param: ?employee_id=X
    
    def perform_create(self, serializer):
        # Set employee from authenticated user
        # Additional security checks
```

**API Endpoints** (via DefaultRouter)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/locations/` | List all locations (filtered by user) | Yes |
| POST | `/api/locations/` | Create new location record | Yes |
| GET | `/api/locations/{id}/` | Retrieve specific location | Yes |
| GET | `/api/locations/?employee_id=X` | Filter by employee ID | Yes |

### 3. Permission System

**Custom Permission** (`location/permissions.py`)

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Employees can only access their own records
        return obj.employee == request.user
```

**Authentication Flow:**
1. User authenticates via Django session or DRF Token
2. Token/session included in API requests
3. ViewSet checks `IsAuthenticated` permission
4. Custom permission validates ownership for object-level access

### 4. Frontend Components

**Track Location Page** (`templates/track_location.html`)

- Button: "Track my location"
- JavaScript uses `navigator.geolocation.getCurrentPosition()`
- On success: POST to `/api/locations/` with lat, long, accuracy
- On error: Display user-friendly error message
- Shows loading state during GPS acquisition
- Displays success/error feedback

**Location History Page** (`templates/location_history.html`)

- Table displaying location records
- Columns: Timestamp, Latitude, Longitude, Accuracy
- Fetches data via GET `/api/locations/`
- Implements pagination for large datasets
- Shows "No records" message when empty
- Auto-refresh option (optional enhancement)

**Frontend-Backend Communication:**
- Uses Fetch API for HTTP requests
- Includes CSRF token for POST requests
- Handles authentication via session cookies
- Implements error handling for network failures

## Data Models

### Location Table Schema

```sql
CREATE TABLE location_location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    accuracy DECIMAL(10, 2) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES auth_user(id),
    INDEX idx_employee_timestamp (employee_id, timestamp DESC),
    INDEX idx_timestamp (timestamp)
);
```

### Sample Data Generation

A Django management command will generate 50 sample records:
- 5-10 different employee IDs
- Random coordinates within realistic ranges
- Accuracy values between 5-50 meters
- Timestamps spread over the past 30 days
- Ensures data diversity for testing

## Error Handling

### Validation Errors

**Coordinate Validation:**
- Latitude: Must be between -90 and 90
- Longitude: Must be between -180 and 180
- Accuracy: Must be positive number
- Returns HTTP 400 with specific error messages

**Example Error Response:**
```json
{
    "latitude": ["Latitude must be between -90 and 90 degrees"],
    "accuracy": ["Accuracy must be a positive number"]
}
```

### Authentication Errors

- HTTP 401: User not authenticated
- HTTP 403: User attempting to access another employee's records
- Clear error messages guide user to login

### GPS Errors (Frontend)

- Permission denied: "Please enable location access in your browser"
- Position unavailable: "Unable to retrieve your location. Please try again"
- Timeout: "Location request timed out. Please try again"

### Server Errors

- HTTP 500: Generic error message to client, detailed logging on server
- Database errors: Caught and logged, user sees friendly message
- Network errors: Frontend displays retry option

### Security Validations

**Input Sanitization:**
- DRF serializers automatically handle SQL injection prevention
- Django templates auto-escape HTML to prevent XSS
- CSRF protection enabled for all POST requests

**Authorization Checks:**
- Every API request validates authentication
- Object-level permissions prevent cross-employee access
- Employee ID in POST requests validated against authenticated user

**Rate Limiting (Optional Enhancement):**
- Throttle location tracking to prevent abuse
- Example: 100 requests per hour per user

## Testing Strategy

### Unit Tests

**Model Tests:**
- Test Location model creation and validation
- Test model methods and properties
- Test database constraints

**Serializer Tests:**
- Test latitude/longitude validation ranges
- Test accuracy validation (positive numbers)
- Test employee_id handling
- Test read-only fields

**ViewSet Tests:**
- Test queryset filtering by authenticated user
- Test permission enforcement
- Test create, list, retrieve operations

### Integration Tests

**API Endpoint Tests:**
- Test POST `/api/locations/` with valid data
- Test POST with invalid coordinates
- Test GET `/api/locations/` returns only user's records
- Test GET with employee_id filter
- Test authentication requirements
- Test permission denials for other users' data

**Frontend Integration:**
- Test GPS API integration (mock geolocation)
- Test API communication
- Test error handling flows
- Test UI updates on success/failure

### Security Tests

- Test SQL injection attempts (should be blocked)
- Test XSS attempts (should be escaped)
- Test unauthorized access attempts
- Test CSRF protection
- Test cross-employee data access (should be denied)

### Test Data

- Use Django fixtures for consistent test data
- Mock GPS coordinates for frontend tests
- Test with edge cases (boundary coordinates, zero accuracy)

### Testing Tools

- Django TestCase for backend tests
- DRF APITestCase for API tests
- Coverage.py for code coverage reporting
- Manual testing for GPS functionality (requires real device)

## Deployment Considerations

**Environment Variables:**
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Configure for production domain
- `DATABASE_URL`: PostgreSQL connection string

**Security Checklist:**
- HTTPS enabled for production
- CORS configured if frontend is separate domain
- Rate limiting implemented
- Database backups configured
- Logging configured for security events

**Performance:**
- Database indexes on employee_id and timestamp
- Pagination for location history
- Consider caching for frequently accessed data

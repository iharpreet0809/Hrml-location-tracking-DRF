# HRMS Location Tracking Module

A Django-based location tracking system for HRMS applications with GPS tracking, location history, and RESTful API endpoints.

## Features

- ✅ Real GPS location tracking (no hardcoded values)
- ✅ High-accuracy GPS with 7 decimal places (~1.1cm precision)
- ✅ GPS accuracy measurement (uncertainty radius in meters)
- ✅ Location history with pagination
- ✅ RESTful API with 3 endpoints (list, create, retrieve)
- ✅ 50 sample location records in database
- ✅ Comprehensive security validations
- ✅ Error handling and logging
- ✅ Responsive UI design
- ✅ Django REST Framework with ModelViewSet + DefaultRouter

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite (with 50 sample records)
- **Frontend**: HTML5, JavaScript (Vanilla JS), CSS
- **Authentication**: Django Session Authentication

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE hrms_location_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update with your MySQL credentials:

```bash
cp .env.example .env
```

Edit `.env` file:
```env
DB_NAME=hrms_location_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Employees

```bash
# Option 1: Create only employees
python manage.py create_employees

# Option 2: Create employees + 50 sample location records
python manage.py populate_locations
```

This creates:
- 10 employees (emp01-emp10)
- Password: `employee` (same for all)
- 50 location records with realistic GPS data (if using populate_locations)

### 6. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Suggested admin credentials:
- Username: `admin`
- Password: `admin123`

### 7. Run Development Server

```bash
python manage.py runserver
```

**For detailed MySQL setup instructions, see `MYSQL_SETUP_GUIDE.md`**

## GPS Accuracy Explained

### What is "Accuracy"?

The accuracy field shows the **GPS uncertainty radius in meters**. It tells you how confident the GPS is about your location.

- **5-10m**: Excellent (GPS satellites, outdoors)
- **10-50m**: Good (GPS satellites)
- **50-100m**: Fair (WiFi/Cell towers)
- **100m+**: Poor (Cell towers only)

### Coordinate Precision

We capture coordinates with **7 decimal places**:
- 7 decimal places = ~1.1 cm precision
- Example: `22.9843560°, 72.3902940°`

### For Best GPS Accuracy

1. ✅ Enable GPS on your device
2. ✅ Go outdoors with clear sky view
3. ✅ Wait 10-30 seconds for GPS lock
4. ✅ Allow browser location access

See `GPS_ACCURACY_GUIDE.md` for detailed information.

## Usage

### Access the Application

1. **Track Location**: http://127.0.0.1:8000/track/
   - Click "Track my location" button
   - Allow browser GPS access
   - Location will be saved automatically

2. **Location History**: http://127.0.0.1:8000/history/
   - View all your tracked locations
   - Paginated table with timestamps

3. **Admin Panel**: http://127.0.0.1:8000/admin/
   - Manage users and locations
   - View all location records

### Login Credentials

**Sample Employees:**
- Username: emp01, emp02, ..., emp10
- Password: employee

**Admin:**
- Username: admin
- Password: admin123

## API Endpoints

✅ **5 API Endpoints (3 Core + 2 Employee Endpoints)**

### Core Location Endpoints

### 1. List Locations (GET) - Filter by Employee ID
```
GET /api/locations/
GET /api/locations/?employee_id=1
```
Returns paginated list of authenticated user's locations.

**Query Parameters:**
- `employee_id`: Filter by employee ID (must match authenticated user)
- `page`: Page number for pagination

**Response:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/locations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee_id": 1,
      "employee_name": "emp001",
      "latitude": "40.7128000",
      "longitude": "-74.0060000",
      "accuracy": "15.50",
      "timestamp": "2024-11-14T10:30:00Z"
    }
  ]
}
```

### 2. Create Location (POST) - With Lat, Long, Accuracy
```
POST /api/locations/
Content-Type: application/json
X-CSRFToken: <csrf_token>

{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "accuracy": 15.5
}
```

**Fields:**
- `latitude`: Latitude coordinate (validated: -90 to 90)
- `longitude`: Longitude coordinate (validated: -180 to 180)
- `accuracy`: GPS accuracy in meters (validated: positive number)
- `employee_id`: Auto-set from authenticated user

**Response:**
```json
{
  "id": 51,
  "employee_id": 1,
  "employee_name": "emp001",
  "latitude": "40.7128000",
  "longitude": "-74.0060000",
  "accuracy": "15.50",
  "timestamp": "2024-11-14T10:35:00Z"
}
```

### 3. Retrieve Location (GET) - By ID
```
GET /api/locations/{id}/
```
Returns specific location record (only if owned by authenticated user).

**Response:**
```json
{
  "id": 1,
  "employee_id": 1,
  "employee_name": "emp001",
  "latitude": "40.7128000",
  "longitude": "-74.0060000",
  "accuracy": "15.50",
  "timestamp": "2024-11-14T10:35:00Z"
}
```

### Additional Employee Endpoints

#### 4. Get Current Employee Info (GET)
```
GET /api/employee/
```
Returns current employee's information and location count.

**Response:**
```json
{
  "employee_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "location_count": 15,
  "is_active": true
}
```

#### 5. List All Employees (GET)
```
GET /api/employees/
```
Returns list of all employees with location tracking data.

**Response:**
```json
[
  {
    "employee_id": 1,
    "username": "emp001",
    "location_count": 15,
    "latest_location": {
      "latitude": "22.9843560",
      "longitude": "72.3902940",
      "accuracy": "15.50",
      "timestamp": "2024-11-14T10:30:00Z"
    }
  }
]
```

### Test the API

Run the test script:
```bash
python test_api.py
```

See `API_DOCUMENTATION.md` for complete API reference.

## Security Features

### Input Validation
- Latitude range: -90 to 90 degrees
- Longitude range: -180 to 180 degrees
- Accuracy: Must be positive number
- All inputs sanitized by DRF serializers

### Authentication & Authorization
- Session-based authentication required
- Users can only access their own location records
- Object-level permissions prevent cross-user access
- Employee ID spoofing prevention

### Protection Against Common Attacks
- ✅ SQL Injection: Django ORM protection
- ✅ XSS: Django template auto-escaping
- ✅ CSRF: Token validation on all POST requests
- ✅ Clickjacking: X-Frame-Options header
- ✅ Unauthorized Access: Permission checks on all endpoints

### Error Handling
- User-friendly error messages
- Detailed server-side logging
- No sensitive information exposed in errors
- GPS error handling (permission denied, timeout, unavailable)

## Project Structure

```
hrms_tracking/
├── hrms_project/          # Django project
│   ├── settings.py        # Configuration
│   └── urls.py            # Main URL routing
├── location/              # Location tracking app
│   ├── models.py          # Location model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets
│   ├── permissions.py     # Custom permissions
│   ├── urls.py            # API routing
│   └── management/
│       └── commands/
│           └── populate_locations.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── track_location.html
│   └── location_history.html
├── static/                # Static files
│   └── css/
│       └── style.css
├── logs/                  # Error logs
├── db.sqlite3             # Database
├── manage.py
└── requirements.txt
```

## Database Schema

### Location Model
```python
- id: AutoField (Primary Key)
- employee: ForeignKey(User)
- latitude: DecimalField(9, 6)
- longitude: DecimalField(9, 6)
- accuracy: DecimalField(10, 2)
- timestamp: DateTimeField (auto_now_add)

Indexes:
- (employee, timestamp DESC)
- (timestamp)
```

## Testing

### Manual Testing

1. **GPS Tracking:**
   - Login as emp001
   - Go to /track/
   - Click "Track my location"
   - Verify location is saved

2. **Location History:**
   - Go to /history/
   - Verify locations are displayed
   - Test pagination

3. **API Testing:**
   ```bash
   # Login first to get session cookie
   curl -X POST http://127.0.0.1:8000/api/locations/ \
     -H "Content-Type: application/json" \
     -H "X-CSRFToken: <token>" \
     -d '{"latitude": 40.7128, "longitude": -74.0060, "accuracy": 15.5}'
   ```

### Security Testing

1. **Cross-user access:**
   - Login as emp001
   - Try to access emp002's locations (should fail)

2. **Invalid coordinates:**
   - Try latitude > 90 or < -90 (should fail)
   - Try longitude > 180 or < -180 (should fail)

3. **Negative accuracy:**
   - Try accuracy <= 0 (should fail)

## Deployment Considerations

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set strong `SECRET_KEY`
5. Enable HTTPS
6. Configure proper CORS settings
7. Set up rate limiting
8. Configure database backups

## License

This project is for demonstration purposes.

## Support

For issues or questions, please contact the development team.

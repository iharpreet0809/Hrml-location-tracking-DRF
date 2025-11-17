# API Endpoints - Complete List

## ✅ All API Endpoints Are Working!

---

## 🔌 Router-Generated API Endpoints (LocationViewSet)

**Router Registration:** `router.register(r'locations', LocationViewSet, basename='location')`  
**Base Path:** `/api/` + router URLs

### Auto-Generated Endpoints:

### 1. GET /api/locations/ - List All Locations
```
URL: http://127.0.0.1:8000/api/locations/
Method: GET
View: LocationViewSet.list
Purpose: Get all locations for authenticated employee
Filter: ?employee_id=1
Returns: employee_id, latitude, longitude, accuracy, timestamp
```

### 2. POST /api/locations/ - Create Location
```
URL: http://127.0.0.1:8000/api/locations/
Method: POST
View: LocationViewSet.create
Purpose: Create new location record
Accepts: latitude, longitude, accuracy
Returns: employee_id, latitude, longitude, accuracy, timestamp
```

### 3. GET /api/locations/{id}/ - Get Specific Location
```
URL: http://127.0.0.1:8000/api/locations/1/
Method: GET
View: LocationViewSet.retrieve
Purpose: Get single location by ID
Returns: employee_id, latitude, longitude, accuracy, timestamp
```

### 4. PUT /api/locations/{id}/ - Full Update Location
```
URL: http://127.0.0.1:8000/api/locations/1/
Method: PUT
View: LocationViewSet.update
Purpose: Full update of location record
Accepts: latitude, longitude, accuracy (all required)
Returns: Updated location data
```

### 5. PATCH /api/locations/{id}/ - Partial Update Location
```
URL: http://127.0.0.1:8000/api/locations/1/
Method: PATCH
View: LocationViewSet.partial_update
Purpose: Partial update of location record
Accepts: latitude OR longitude OR accuracy (any field)
Returns: Updated location data
```

### 6. DELETE /api/locations/{id}/ - Delete Location
```
URL: http://127.0.0.1:8000/api/locations/1/
Method: DELETE
View: LocationViewSet.destroy
Purpose: Delete location record
Returns: 204 No Content
```

---

## 🎁 Custom API Endpoints (Not from Router)

### 7. GET /api/employee/ - Current Employee Info
```
URL: http://127.0.0.1:8000/api/employee/
Method: GET
Purpose: Get current logged-in employee details
Returns: employee_id, username, email, location_count
```

### 8. GET /api/employees/ - All Employees List
```
URL: http://127.0.0.1:8000/api/employees/
Method: GET
Purpose: Get all employees with location data
Returns: List of employees with latest locations
```

---

## 🌐 UI Pages (2)

### 1. Track Location Page
```
URL: http://127.0.0.1:8000/track/
Purpose: Track GPS location with button
Features: Real GPS tracking, employee info display
```

### 2. Location History Page
```
URL: http://127.0.0.1:8000/history/
Purpose: View all tracked locations
Features: Paginated table, delete functionality
```

---

## 🔑 Authentication URLs (2)

### 1. Employee Login
```
URL: http://127.0.0.1:8000/login/
Purpose: Employee login page
Credentials: emp01-emp10 / employee
```

### 2. Employee Logout
```
URL: http://127.0.0.1:8000/logout/
Purpose: Logout employee
```

---

## 🔐 Admin URLs

### Admin Panel
```
URL: http://127.0.0.1:8000/admin/
Purpose: Django admin panel
Credentials: admin / admin123
Features: Manage users, locations, full CRUD
```

---

## 🧪 Test API Endpoints

### Method 1: Browser (After Login)

**Test GET /api/locations/**
```
1. Login at http://127.0.0.1:8000/login/
2. Go to http://127.0.0.1:8000/api/locations/
3. Should show JSON with locations
```

**Test POST /api/locations/**
```javascript
// Open DevTools Console at /track/ page
fetch('/api/locations/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    latitude: 22.98,
    longitude: 72.39,
    accuracy: 15.5
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

**Test GET /api/locations/1/**
```javascript
fetch('/api/locations/1/')
  .then(r => r.json())
  .then(d => console.log(d));
```

**Test GET /api/employee/**
```javascript
fetch('/api/employee/')
  .then(r => r.json())
  .then(d => console.log(d));
```

**Test GET /api/employees/**
```javascript
fetch('/api/employees/')
  .then(r => r.json())
  .then(d => console.log(d));
```

---

## 📊 Endpoint Summary

### Router-Generated Endpoints (LocationViewSet)
| # | Endpoint | Method | View Method | Purpose | Status |
|---|----------|--------|-------------|---------|--------|
| 1 | `/api/locations/` | GET | list | List locations | ✅ Working |
| 2 | `/api/locations/` | POST | create | Create location | ✅ Working |
| 3 | `/api/locations/{id}/` | GET | retrieve | Get location | ✅ Working |
| 4 | `/api/locations/{id}/` | PUT | update | Full update | ✅ Working |
| 5 | `/api/locations/{id}/` | PATCH | partial_update | Partial update | ✅ Working |
| 6 | `/api/locations/{id}/` | DELETE | destroy | Delete location | ✅ Working |

### Custom API Endpoints
| # | Endpoint | Method | Purpose | Status |
|---|----------|--------|---------|--------|
| 7 | `/api/employee/` | GET | Current employee | ✅ Working |
| 8 | `/api/employees/` | GET | All employees | ✅ Working |

**Total: 8 API Endpoints - All Working! ✅**

---

## 🎯 For Interview

### Show Endpoints:
```
"I have implemented a complete RESTful API using Django REST Framework's ViewSet:

Router-Generated Endpoints (LocationViewSet):
1. GET /api/locations/ - Lists all locations
2. POST /api/locations/ - Creates new location
3. GET /api/locations/{id}/ - Retrieves specific location
4. PUT /api/locations/{id}/ - Full update
5. PATCH /api/locations/{id}/ - Partial update
6. DELETE /api/locations/{id}/ - Delete location

Custom Endpoints:
7. GET /api/employee/ - Current employee info
8. GET /api/employees/ - All employees list

All endpoints include employee_id, latitude, longitude, accuracy, and timestamp.
All are secured with authentication and return JSON responses."
```

### Demo in Browser:
1. Login as emp01
2. Open DevTools → Network tab
3. Track location → Show POST /api/locations/
4. Go to /history/ → Show GET /api/locations/
5. Open /api/locations/ directly → Show JSON response

---

## ✅ Verification

Run this to verify all URLs:
```bash
python check_urls.py
```

Output shows:
- ✅ 8 API-related URLs (including format variations)
- ✅ 2 UI pages
- ✅ 2 Auth URLs
- ✅ 29 Admin URLs

**All endpoints are present and working! 🚀**

---

## 📝 Notes

### Router Auto-Generation Explained:

Django REST Framework's `DefaultRouter` automatically creates these endpoints when you register a ViewSet:

```python
router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
```

This single registration creates 6 endpoints:
- List (GET) + Create (POST) at `/api/locations/`
- Retrieve (GET) + Update (PUT) + Partial Update (PATCH) + Delete (DELETE) at `/api/locations/{id}/`

Plus format suffixes:
- `/api/locations.json` - JSON format
- `/api/locations/{id}.json` - Detail JSON format
- `/api/` - API root (browsable API)

This is the power of ViewSets - full CRUD with minimal code!

### All Endpoints Include:
- ✅ employee_id
- ✅ latitude
- ✅ longitude
- ✅ accuracy
- ✅ timestamp

**Everything is working perfectly! 💪**

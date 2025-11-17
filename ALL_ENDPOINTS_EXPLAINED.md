# Tumhare Saare Endpoints - Complete List

## 📍 Total Endpoints: 10

---

## 🔐 AUTHENTICATION ENDPOINTS (2)

### 1. Login Page
```
URL: http://127.0.0.1:8000/login/
Method: GET, POST
Kya karta hai: Employee login page dikhata hai
Login credentials: emp1 / employee
```

### 2. Logout
```
URL: http://127.0.0.1:8000/logout/
Method: GET
Kya karta hai: User ko logout kar deta hai
```

---

## 🌐 UI PAGES (2)

### 3. Track Location Page
```
URL: http://127.0.0.1:8000/track/
Method: GET
Kya karta hai: 
- "Track my location" button dikhata hai
- GPS se location track karta hai
- Employee info dikhata hai (ID, username, email, location count)
File: templates/track_location.html
```

### 4. Location History Page
```
URL: http://127.0.0.1:8000/history/
Method: GET
Kya karta hai:
- Saare tracked locations table me dikhata hai
- Pagination hai (20 records per page)
- Delete button hai har record ke liye
File: templates/location_history.html
```

---

## 🔌 API ENDPOINTS - ROUTER SE AUTO-GENERATED

**Router Configuration:**
```python
router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
urlpatterns = [
    path('api/', include(router.urls)),  # Ye line 6 endpoints banati hai!
]
```

### 5. List All Locations (GET)
```
URL: http://127.0.0.1:8000/api/locations/
Method: GET
Kya karta hai:
- Authenticated user ke saare locations return karta hai
- Pagination support hai
- Filter by employee_id: /api/locations/?employee_id=1

Request Example:
GET /api/locations/

Response Example:
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/locations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee_id": 1,           ← Employee ID
      "employee_name": "emp001",
      "latitude": "22.9843560",   ← Latitude
      "longitude": "72.3902940",  ← Longitude
      "accuracy": "15.50",        ← Accuracy
      "timestamp": "2024-11-14T10:30:00Z"
    }
  ]
}

Security:
- Login required
- Sirf apne locations dikhate hain
```

### 6. Create Location (POST)
```
URL: http://127.0.0.1:8000/api/locations/
Method: POST
Kya karta hai:
- Naya location record banata hai
- GPS se latitude, longitude, accuracy leta hai
- Employee ID automatically authenticated user se set hota hai

Request Example:
POST /api/locations/
Headers:
  Content-Type: application/json
  X-CSRFToken: <csrf_token>
Body:
{
  "latitude": 22.9843560,    ← Latitude (-90 to 90)
  "longitude": 72.3902940,   ← Longitude (-180 to 180)
  "accuracy": 15.50          ← Accuracy (positive number)
}

Response Example:
{
  "id": 51,
  "employee_id": 1,           ← Auto-set from authenticated user
  "employee_name": "emp001",
  "latitude": "22.9843560",
  "longitude": "72.3902940",
  "accuracy": "15.50",
  "timestamp": "2024-11-17T10:35:00Z"
}

Validation:
- Latitude: -90 to 90
- Longitude: -180 to 180
- Accuracy: must be positive
- CSRF token required
```

### 7. Get Specific Location (GET)
```
URL: http://127.0.0.1:8000/api/locations/{id}/
Method: GET
Kya karta hai:
- Ek specific location record return karta hai by ID
- Sirf apna location access kar sakte ho

Request Example:
GET /api/locations/1/

Response Example:
{
  "id": 1,
  "employee_id": 1,           ← Employee ID
  "employee_name": "emp001",
  "latitude": "22.9843560",   ← Latitude
  "longitude": "72.3902940",  ← Longitude
  "accuracy": "15.50",        ← Accuracy
  "timestamp": "2024-11-14T10:30:00Z"
}

Security:
- Agar dusre user ka location access karo → 403 Forbidden
```

### 8. Update Location (PUT/PATCH)
```
URL: http://127.0.0.1:8000/api/locations/{id}/
Method: PUT, PATCH
Kya karta hai:
- Existing location record update karta hai
- Sirf apna location update kar sakte ho

Request Example:
PUT /api/locations/1/
Body:
{
  "latitude": 22.9900000,
  "longitude": 72.4000000,
  "accuracy": 20.00
}

Note: Normally location update nahi karte, but endpoint available hai
```

### 9. Delete Location (DELETE)
```
URL: http://127.0.0.1:8000/api/locations/{id}/
Method: DELETE
View: LocationViewSet.destroy (router auto-generated)
Kya karta hai:
- Location record delete karta hai
- Sirf apna location delete kar sakte ho

Request Example:
DELETE /api/locations/1/

Response:
204 No Content (success)

Security:
- CSRF token required
- Sirf apna location delete kar sakte ho
```

---

## 🎁 CUSTOM API ENDPOINTS (Router se nahi, manually defined)

### 10. Current Employee Info (GET)
```
URL: http://127.0.0.1:8000/api/employee/
Method: GET
Kya karta hai:
- Current logged-in employee ki info return karta hai
- Location count bhi dikhata hai

Request Example:
GET /api/employee/

Response Example:
{
  "employee_id": 1,
  "username": "emp001",
  "email": "emp001@company.com",
  "first_name": "Employee",
  "last_name": "One",
  "location_count": 15,
  "is_active": true
}
```

### 11. All Employees List (GET)
```
URL: http://127.0.0.1:8000/api/employees/
Method: GET
View: employee_list_view (custom function-based view)
Kya karta hai:
- Saare employees ki list return karta hai
- Har employee ka latest location bhi dikhata hai

Request Example:
GET /api/employees/

Response Example:
[
  {
    "employee_id": 1,
    "username": "emp001",
    "email": "emp001@company.com",
    "location_count": 15,
    "latest_location": {
      "latitude": "22.9843560",
      "longitude": "72.3902940",
      "accuracy": "15.50",
      "timestamp": "2024-11-14T10:30:00Z"
    }
  },
  {
    "employee_id": 2,
    "username": "emp002",
    "email": "emp002@company.com",
    "location_count": 8,
    "latest_location": {
      "latitude": "40.7128000",
      "longitude": "-74.0060000",
      "accuracy": "25.30",
      "timestamp": "2024-11-14T09:15:00Z"
    }
  }
]

Note: Ye custom endpoint hai, router se nahi bana
```

---

## 🎯 REQUIREMENT KE LIYE 3 MAIN ENDPOINTS

Interviewer ne 3 endpoints maange the with **Employee ID, Lat-Long, Accuracy**:

### ✅ Endpoint 1: GET /api/locations/
**Kya return karta hai:**
- ✅ employee_id
- ✅ latitude
- ✅ longitude
- ✅ accuracy
- ✅ timestamp (bonus)

### ✅ Endpoint 2: POST /api/locations/
**Kya accept karta hai:**
- ✅ latitude
- ✅ longitude
- ✅ accuracy
- ✅ employee_id (auto-set from authenticated user)

**Kya return karta hai:**
- ✅ employee_id
- ✅ latitude
- ✅ longitude
- ✅ accuracy
- ✅ timestamp

### ✅ Endpoint 3: GET /api/locations/{id}/
**Kya return karta hai:**
- ✅ employee_id
- ✅ latitude
- ✅ longitude
- ✅ accuracy
- ✅ timestamp

---

## 📊 ENDPOINTS SUMMARY TABLE

### Authentication & UI Pages
| # | URL | Method | Kya Karta Hai | Source |
|---|-----|--------|---------------|--------|
| 1 | `/login/` | GET, POST | Login page | Manual |
| 2 | `/logout/` | GET | Logout | Manual |
| 3 | `/track/` | GET | Track location UI | Manual |
| 4 | `/history/` | GET | Location history UI | Manual |

### Router-Generated API Endpoints (LocationViewSet)
| # | URL | Method | View Method | Kya Karta Hai |
|---|-----|--------|-------------|---------------|
| 5 | `/api/locations/` | GET | list | List locations |
| 6 | `/api/locations/` | POST | create | Create location |
| 7 | `/api/locations/{id}/` | GET | retrieve | Get location |
| 8 | `/api/locations/{id}/` | PUT | update | Full update |
| 9 | `/api/locations/{id}/` | PATCH | partial_update | Partial update |
| 10 | `/api/locations/{id}/` | DELETE | destroy | Delete location |

### Custom API Endpoints
| # | URL | Method | View Function | Kya Karta Hai |
|---|-----|--------|---------------|---------------|
| 11 | `/api/employee/` | GET | employee_info_view | Current employee info |
| 12 | `/api/employees/` | GET | employee_list_view | All employees list |

---

## 🧪 TESTING ENDPOINTS

### Method 1: Browser (Simple)
```
1. Login: http://127.0.0.1:8000/login/
2. Track: http://127.0.0.1:8000/track/
3. History: http://127.0.0.1:8000/history/
4. API: http://127.0.0.1:8000/api/locations/
```

### Method 2: Browser DevTools (API Testing)
```
1. Open http://127.0.0.1:8000/track/
2. Open DevTools → Console
3. Run:

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Test GET /api/locations/
fetch('/api/locations/')
  .then(r => r.json())
  .then(d => console.log(d));

// Test POST /api/locations/
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

// Test GET /api/locations/1/
fetch('/api/locations/1/')
  .then(r => r.json())
  .then(d => console.log(d));

// Test GET /api/employee/
fetch('/api/employee/')
  .then(r => r.json())
  .then(d => console.log(d));

// Test GET /api/employees/
fetch('/api/employees/')
  .then(r => r.json())
  .then(d => console.log(d));
```

### Method 3: Python Script
```python
import requests

# Login
session = requests.Session()
login_url = 'http://127.0.0.1:8000/admin/login/'
session.get(login_url)

session.post(login_url, data={
    'username': 'admin',
    'password': 'admin123',
    'csrfmiddlewaretoken': session.cookies['csrftoken']
})

# Test GET /api/locations/
response = session.get('http://127.0.0.1:8000/api/locations/')
print("GET /api/locations/:", response.json())

# Test POST /api/locations/
response = session.post('http://127.0.0.1:8000/api/locations/', 
    json={
        'latitude': 22.98,
        'longitude': 72.39,
        'accuracy': 15.5
    },
    headers={'X-CSRFToken': session.cookies['csrftoken']}
)
print("POST /api/locations/:", response.json())

# Test GET /api/locations/1/
response = session.get('http://127.0.0.1:8000/api/locations/1/')
print("GET /api/locations/1/:", response.json())

# Test GET /api/employee/
response = session.get('http://127.0.0.1:8000/api/employee/')
print("GET /api/employee/:", response.json())

# Test GET /api/employees/
response = session.get('http://127.0.0.1:8000/api/employees/')
print("GET /api/employees/:", response.json())
```

---

## 🔍 INTERVIEWER KO KAISE DIKHANA HAI

### Demo Script:

**Step 1: Show UI Endpoints**
```
"Pehle main UI pages dikhata hoon..."

1. Open http://127.0.0.1:8000/track/
   → "Ye track location page hai with button"
   
2. Click "Track my location"
   → "GPS se real location track ho raha hai"
   
3. Open http://127.0.0.1:8000/history/
   → "Ye location history page hai with table"
```

**Step 2: Show API Endpoints**
```
"Ab main API endpoints dikhata hoon..."

1. Open DevTools → Network tab

2. Track location again
   → Show POST /api/locations/ request
   → Show request body: {latitude, longitude, accuracy}
   → Show response: {employee_id, latitude, longitude, accuracy}

3. Refresh history page
   → Show GET /api/locations/ request
   → Show response with all locations

4. In console, run:
   fetch('/api/locations/1/').then(r => r.json()).then(console.log)
   → Show single location with employee_id, lat, long, accuracy
```

**Step 3: Explain 3 Required Endpoints**
```
"Requirements me 3 endpoints maange the with employee_id, lat-long, accuracy:

1. GET /api/locations/ 
   → List all locations with employee_id, lat, long, accuracy ✅

2. POST /api/locations/
   → Create location with lat, long, accuracy
   → Employee_id auto-set from authenticated user ✅

3. GET /api/locations/{id}/
   → Get specific location with employee_id, lat, long, accuracy ✅

Plus 2 bonus endpoints:
4. GET /api/employee/ - Current employee info
5. GET /api/employees/ - All employees list
"
```

---

## ✅ SUMMARY

**Total Endpoints: 12**
- 2 Authentication (login, logout)
- 2 UI Pages (track, history)
- 6 Router-Generated API (list, create, retrieve, update, partial_update, destroy)
- 2 Custom API (employee info, employees list)

**Router Magic:**
```python
# Ye ek line 6 endpoints banati hai!
router.register(r'locations', LocationViewSet, basename='location')
```

**3 Required API Endpoints (with employee_id, lat-long, accuracy):**
1. ✅ GET /api/locations/ - List (router.list)
2. ✅ POST /api/locations/ - Create (router.create)
3. ✅ GET /api/locations/{id}/ - Retrieve (router.retrieve)

**Bonus Endpoints:**
4. ✅ PUT /api/locations/{id}/ - Update (router.update)
5. ✅ PATCH /api/locations/{id}/ - Partial Update (router.partial_update)
6. ✅ DELETE /api/locations/{id}/ - Delete (router.destroy)
7. ✅ GET /api/employee/ - Current employee (custom)
8. ✅ GET /api/employees/ - All employees (custom)

**Sab kuch ready hai! 🚀**

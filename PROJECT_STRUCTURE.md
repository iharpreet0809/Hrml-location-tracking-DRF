# HRMS Location Tracking - Project Structure

## 📁 Project Files

```
hrms_tracking/
│
├── 📄 manage.py                          # Django management script
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .env                              # Environment variables (MySQL credentials)
├── 📄 .env.example                      # Environment variables template
├── 📄 .gitignore                        # Git ignore rules
├── 📄 setup_mysql.sql                   # MySQL database setup script
│
├── 📖 README.md                         # Main documentation
├── 📖 QUICK_START.md                    # Quick setup guide
├── 📖 ALL_ENDPOINTS_EXPLAINED.md        # Complete API documentation
│
├── 📁 hrms_project/                     # Django project settings
│   ├── __init__.py
│   ├── settings.py                      # Main settings (reads from .env)
│   ├── urls.py                          # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── 📁 location/                         # Location tracking app
│   ├── __init__.py
│   ├── admin.py                         # Django admin configuration
│   ├── apps.py
│   ├── models.py                        # Location model (database schema)
│   ├── serializers.py                   # DRF serializers (validation)
│   ├── views.py                         # API views and UI views
│   ├── urls.py                          # URL routing
│   ├── permissions.py                   # Custom permissions
│   ├── tests.py
│   │
│   ├── 📁 migrations/                   # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   └── 📁 management/                   # Management commands
│       ├── __init__.py
│       └── 📁 commands/
│           ├── __init__.py
│           ├── create_employees.py      # Create 10 employees ✅
│           └── populate_locations.py    # Create employees + 50 locations
│
├── 📁 templates/                        # HTML templates
│   ├── base.html                        # Base template
│   ├── login.html                       # Login page
│   ├── track_location.html              # Track location page ✅
│   └── location_history.html            # Location history page ✅
│
├── 📁 static/                           # Static files (CSS, JS)
│   └── 📁 css/
│       └── style.css                    # Custom styles
│
└── 📁 logs/                             # Error logs
    └── errors.log                       # Application error logs
```

---

## 📋 File Descriptions

### Core Files

**manage.py**
- Django management script
- Run commands: `python manage.py <command>`

**requirements.txt**
- Python dependencies
- Install: `pip install -r requirements.txt`

**.env**
- Environment variables (MySQL credentials)
- **IMPORTANT**: Update `DB_PASSWORD` with your MySQL password
- Not committed to Git (in .gitignore)

**.env.example**
- Template for .env file
- Safe to commit to Git
- Copy to .env and update values

**.gitignore**
- Files to ignore in Git
- Includes .env, logs, __pycache__, etc.

**setup_mysql.sql**
- MySQL database creation script
- Run: `mysql -u root -p < setup_mysql.sql`

---

### Documentation Files

**README.md**
- Main project documentation
- Installation and setup instructions
- Features and usage

**QUICK_START.md**
- Fast 5-minute setup guide
- Quick commands
- Troubleshooting

**ALL_ENDPOINTS_EXPLAINED.md**
- Complete API documentation
- All 5 endpoints explained
- Request/response examples
- Testing instructions

---

### Django Project (hrms_project/)

**settings.py**
- Django configuration
- Reads from .env file
- MySQL database configuration
- Security settings
- REST Framework configuration

**urls.py**
- Main URL routing
- Includes location app URLs
- Admin panel URLs

---

### Location App (location/)

**models.py**
- Location model (database schema)
- Fields: employee, latitude, longitude, accuracy, timestamp
- Indexes for performance

**serializers.py**
- DRF serializers
- Input validation (lat, long, accuracy)
- Data transformation

**views.py**
- LocationViewSet (API endpoints)
- track_location_view (UI page)
- location_history_view (UI page)
- employee_info_view (API)
- employee_list_view (API)

**urls.py**
- URL routing for location app
- API endpoints
- UI pages

**permissions.py**
- IsOwnerOrReadOnly permission
- Ensures users can only access their own data

---

### Management Commands (location/management/commands/)

**create_employees.py** ✅
- Creates 10 employees (emp01-emp10)
- Password: employee
- Run: `python manage.py create_employees`

**populate_locations.py**
- Creates 10 employees + 50 location records
- Sample data from major Indian cities
- Run: `python manage.py populate_locations`

---

### Templates (templates/)

**base.html**
- Base template with common HTML structure
- Navigation, styles, scripts

**login.html**
- Employee login page
- Username/password form

**track_location.html** ✅
- Track location page
- "Track my location" button
- Real GPS tracking
- Shows employee info

**location_history.html** ✅
- Location history page
- Paginated table
- Delete functionality

---

### Static Files (static/)

**style.css**
- Custom CSS styles
- Responsive design
- Button styles, table styles, etc.

---

## 🎯 Key Files for Interview

### Must Know:
1. **models.py** - Database schema
2. **views.py** - API logic and UI views
3. **serializers.py** - Validation logic
4. **track_location.html** - GPS tracking implementation
5. **settings.py** - Configuration (MySQL, .env)

### Must Explain:
1. **create_employees.py** - How employees are created
2. **.env** - Why environment variables
3. **ALL_ENDPOINTS_EXPLAINED.md** - API documentation

---

## 📊 Database Tables

### Created by Django:
- `auth_user` - User accounts (employees)
- `auth_group` - User groups
- `auth_permission` - Permissions
- `django_session` - User sessions
- `django_migrations` - Migration history

### Created by Location App:
- `location_location` - Location tracking data ✅
  - id (Primary Key)
  - employee_id (Foreign Key to auth_user)
  - latitude (Decimal 10,7)
  - longitude (Decimal 11,7)
  - accuracy (Decimal 15,2)
  - timestamp (DateTime)

---

## 🚀 Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Setup MySQL database
mysql -u root -p < setup_mysql.sql

# Configure .env
cp .env.example .env
# Edit .env and set DB_PASSWORD

# Run migrations
python manage.py migrate

# Create 10 employees
python manage.py create_employees

# Create employees + 50 locations
python manage.py populate_locations

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## 🔐 Login Credentials

### Employees (10 users):
- Username: emp01, emp02, ..., emp10
- Password: employee

### Admin (after creating):
- Username: admin
- Password: admin123

---

## 📱 URLs

- Login: http://127.0.0.1:8000/login/
- Track: http://127.0.0.1:8000/track/
- History: http://127.0.0.1:8000/history/
- API: http://127.0.0.1:8000/api/locations/
- Admin: http://127.0.0.1:8000/admin/

---

## ✅ Clean Codebase

**Kept Only Essential Files:**
- ✅ Core Django files (manage.py, settings.py, etc.)
- ✅ Location app (models, views, serializers)
- ✅ Templates (track, history)
- ✅ Management commands (create_employees, populate_locations)
- ✅ Documentation (README, QUICK_START, ALL_ENDPOINTS_EXPLAINED)
- ✅ Configuration (.env, requirements.txt, setup_mysql.sql)

**Removed Unnecessary Files:**
- ❌ Duplicate documentation files
- ❌ Test scripts
- ❌ Old SQLite database
- ❌ Temporary files

**Result: Clean, professional, production-ready codebase! 🎉**

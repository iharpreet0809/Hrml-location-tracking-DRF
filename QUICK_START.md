# Quick Start Guide - MySQL Setup

## 🚀 Fast Setup (5 Minutes)

---

## Step 1: Install MySQL Client
```bash
pip install mysqlclient python-dotenv
```

---

## Step 2: Create MySQL Database

### Option A: Using SQL Script (Recommended)
```bash
mysql -u root -p < setup_mysql.sql
```

### Option B: Manual Commands
```bash
mysql -u root -p
```
```sql
CREATE DATABASE hrms_location_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## Step 3: Configure .env File

**Copy example file:**
```bash
cp .env.example .env
```

**Edit `.env` and update:**
```env
DB_PASSWORD=your_mysql_root_password
```

---

## Step 4: Run Migrations & Setup
```bash
# Apply database migrations
python manage.py migrate

# Create 50 sample location records
python manage.py populate_locations

# Create admin user
python manage.py createsuperuser
# Username: admin
# Password: admin123
```

---

## Step 5: Start Server
```bash
python manage.py runserver
```

**Open:** http://127.0.0.1:8000/

**Login:** emp01 / employee

---

## ✅ Done! Your MySQL setup is complete!

### Verify Database:
```bash
mysql -u root -p
```
```sql
USE hrms_location_db;
SHOW TABLES;
SELECT COUNT(*) FROM location_location;  -- Should show 50
EXIT;
```

---

## 🔧 Troubleshooting

### Can't install mysqlclient?
```bash
# Use PyMySQL instead
pip install pymysql

# Add to hrms_project/__init__.py:
import pymysql
pymysql.install_as_MySQLdb()
```

### MySQL not running?
```bash
# Windows
net start MySQL

# Linux
sudo systemctl start mysql

# macOS
brew services start mysql
```

### Wrong password?
Update `.env` file with correct MySQL password:
```env
DB_PASSWORD=your_actual_password
```

---

## 📝 Default Credentials

**MySQL:**
- Database: `hrms_location_db`
- User: `root`
- Password: (your MySQL root password)

**Django Admin:**
- Username: `admin`
- Password: `admin123`

**Sample Employees:**
- Username: `emp01` to `emp10`
- Password: `employee`

---

## 🎯 Next Steps

1. ✅ Login at http://127.0.0.1:8000/login/
2. ✅ Track location at http://127.0.0.1:8000/track/
3. ✅ View history at http://127.0.0.1:8000/history/
4. ✅ Test API at http://127.0.0.1:8000/api/locations/

**You're ready for the interview! 🚀**

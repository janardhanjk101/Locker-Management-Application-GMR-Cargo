# 🔐 Locker Management System

A modern, secure locker management system with a beautiful Apple-inspired UI featuring glassmorphism effects, authentication, and Excel import/export capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## ✨ Features

- 🔒 **Secure Authentication** - Session-based login system
- 🎨 **Modern UI** - Glassmorphism design with black & fire orange theme
- 📊 **Real-time Dashboard** - Live statistics and occupancy tracking
- 🔍 **Advanced Search** - Search across all locker parameters
- 📥 **Excel Import** - Bulk upload locker data
- 📤 **Excel Export** - Download complete database
- ⏰ **Live Clock** - Real-time date and time display
- 💾 **SQLite Database** - Lightweight, no setup required
- 🔄 **Auto-refresh** - Real-time data synchronization

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation:
     ```bash
     python --version
     # or
     python3 --version
     ```

2. **pip** (Python package manager)
   - Usually comes with Python
   - Verify installation:
     ```bash
     pip --version
     # or
     pip3 --version
     ```

### System Requirements

- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 100MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## 🚀 Installation

### Step 1: Download/Clone the Project

Create a project directory and add all files:

```bash
mkdir locker-management
cd locker-management
```

Place these files in the directory:
- `app.py`
- `requirements.txt`
- `templates/login.html`
- `templates/index.html`

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-CORS 4.0.0
- pandas 2.1.4
- openpyxl 3.1.2

### Step 4: Verify Installation

Check if all packages are installed:
```bash
pip list
```

You should see Flask, Flask-CORS, pandas, and openpyxl in the list.

## 🎯 Running the Application

### Start the Server

```bash
python app.py
```

You should see output similar to:
```
============================================================
🔐 Locker Management System Starting...
============================================================
Server running on: http://localhost:5000
Local network access: http://192.168.29.192:5000

Default Login Credentials:
  Username: admin
  Password: admin123
============================================================
```

### Access the Application

1. **Local Access:**
   - Open your browser and go to: `http://localhost:5000`

2. **Network Access:**
   - From other devices on the same network: `http://YOUR_IP:5000`
   - Find your IP: Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

### Login

Use the default credentials:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change these credentials in production!

## 📖 Usage Guide

### Dashboard Overview

After logging in, you'll see:
- **Statistics Cards**: Total, Occupied, and Available lockers
- **Search Bar**: Find lockers instantly
- **Filter Buttons**: View All, Occupied, or Available lockers
- **Locker Grid**: Visual representation of all 300 lockers
- **Live Clock**: Current date and time in the top bar

### Managing Lockers

#### Assign a Locker
1. Click on any empty (green) locker card
2. Fill in the employee details:
   - GC Number
   - Employee Number
   - Name (required)
   - Designation
   - Department
   - Gender
   - From Date
   - To Date
3. Click **Save**

#### Edit a Locker
1. Click on an occupied (orange) locker card
2. Modify the details as needed
3. Click **Save**

#### Clear a Locker
1. Click on any locker card
2. Click **Clear Locker** button
3. Confirm the action

### Excel Import/Export

#### Import Data from Excel

1. Click **📥 Import Excel** button
2. Select your Excel file (.xlsx or .xls)
3. Wait for confirmation message

**Required Excel Format:**

| Column Name | Type | Required | Description |
|------------|------|----------|-------------|
| locker_no | Number | Yes | 1-300 |
| gc_no | Text | No | GC Number |
| emp_no | Text | No | Employee Number |
| name | Text | No* | Employee Name |
| designation | Text | No | Job Title |
| department | Text | No | Department |
| gender | Text | No | Male/Female/Other |
| from_date | Date/Text | No | Start Date |
| to_date | Date/Text | No | End Date |

*If name is empty, locker is marked as available

**Sample Excel Data:**
```
locker_no | gc_no | emp_no | name      | designation | department | gender | from_date  | to_date
1         | GC001 | E001   | John Doe  | Manager     | IT         | Male   | 2024-01-01 | 2024-12-31
2         | GC002 | E002   | Jane Smith| Developer   | IT         | Female | 2024-01-01 | 2024-12-31
```

#### Export Data to Excel

1. Click **📤 Export Excel** button
2. File downloads automatically with timestamp
3. Open with Excel, Google Sheets, or any spreadsheet software

### Search and Filter

**Search:** Type in the search box to find lockers by:
- Locker number
- GC number
- Employee number
- Name
- Designation
- Department

**Filter:** Click filter buttons to view:
- **All**: Show all 300 lockers
- **Occupied**: Show only assigned lockers
- **Available**: Show only empty lockers

## 🗂️ Project Structure

```
locker-management/
│
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── lockers.db            # SQLite database (auto-created)
├── uploads/              # Excel upload folder (auto-created)
│
└── templates/
    ├── login.html        # Login page
    └── index.html        # Main dashboard
```

## 🔧 Configuration

### Change Login Credentials

Edit `app.py` (lines 28-29):

```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_password'
```

### Change Server Port

Edit `app.py` (last line):

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to any port
```

### Change Secret Key

Edit `app.py` (line 11):

```python
app.secret_key = 'your-secure-random-key-here'
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

### Modify Number of Lockers

Edit `app.py` (around line 58):

```python
for i in range(1, 501):  # Change 301 to your desired number + 1
    conn.execute('INSERT INTO lockers (locker_no) VALUES (?)', (i,))
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```
Error: Address already in use
```
**Solution:** Change the port number or kill the process using port 5000:

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Ensure virtual environment is activated and install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. PowerShell Execution Policy (Windows)
```
cannot be loaded because running scripts is disabled
```
**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

#### 4. Login Not Working
**Solution:**
- Clear browser cookies
- Restart the Flask server
- Check browser console (F12) for errors
- Verify credentials match those in `app.py`

#### 5. Excel Import Failed
**Solution:**
- Verify column names match exactly (case-sensitive)
- Check locker_no values are between 1-300
- Ensure file format is .xlsx or .xls
- Remove any special characters from data

#### 6. Database Locked Error
**Solution:**
```bash
# Stop the server and delete the database
rm lockers.db  # Mac/Linux
del lockers.db  # Windows

# Restart the server
python app.py
```

## 💾 Database Management

### Backup Database

**Windows:**
```bash
copy lockers.db lockers_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
```

**Mac/Linux:**
```bash
cp lockers.db lockers_backup_$(date +%Y%m%d).db
```

### Reset Database

```bash
# Delete database file
rm lockers.db     # Mac/Linux
del lockers.db    # Windows

# Restart server (creates fresh database)
python app.py
```

### View Database (Optional)

Install SQLite:
```bash
# Mac
brew install sqlite

# Ubuntu/Debian
sudo apt-get install sqlite3

# Windows - Download from sqlite.org
```

Query database:
```bash
sqlite3 lockers.db
.tables
SELECT * FROM lockers LIMIT 10;
.quit
```

## 🔒 Security Recommendations

### For Production Deployment

1. **Change Default Credentials**
   ```python
   ADMIN_USERNAME = os.environ.get('ADMIN_USER')
   ADMIN_PASSWORD = os.environ.get('ADMIN_PASS')
   ```

2. **Use Environment Variables**
   ```bash
   export SECRET_KEY="your-secure-key"
   export ADMIN_USER="your-username"
   export ADMIN_PASS="your-password"
   ```

3. **Enable HTTPS**
   - Use SSL certificates
   - Set `SESSION_COOKIE_SECURE = True`

4. **Add Password Hashing**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

5. **Disable Debug Mode**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

6. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Opera

## 🤝 Support

### Getting Help

1. Check this README for solutions
2. Review error messages in:
   - Terminal/Command Prompt
   - Browser Console (F12)
3. Verify all prerequisites are met
4. Ensure files are in correct directories

### Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Deactivate virtual environment
deactivate

# Check Python version
python --version

# List installed packages
pip list

# Update pip
python -m pip install --upgrade pip
```

## 📄 License

This project is free to use and modify for your organization.

## 👨‍💻 Developer

**Made by Janardhan**

---

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Project files downloaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Server running on port 5000
- [ ] Logged in successfully
- [ ] Changed default credentials (for production)

## 📞 Need Help?

If you encounter issues:
1. Read the troubleshooting section
2. Check that all prerequisites are installed
3. Verify all files are in the correct locations
4. Ensure the virtual environment is activated
5. Check browser console for JavaScript errors (F12)

---

**Happy Managing! 🚀**
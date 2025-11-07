from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
import pandas as pd
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production-use-secrets-token-hex-32'

# Session configuration - CRITICAL FIX
app.config['SESSION_COOKIE_SAMESITE'] = None  # Changed from 'Lax' to None
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_DOMAIN'] = None  # Allow any domain
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# CORS configuration - allow credentials from any origin in development
CORS(app, supports_credentials=True, origins=['http://localhost:5000', 'http://127.0.0.1:5000', 'http://192.168.29.192:5000'])

# Configuration
DATABASE = 'lockers.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Default credentials (change these!)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS lockers (
                locker_no INTEGER PRIMARY KEY,
                gc_no TEXT,
                emp_no TEXT,
                name TEXT,
                designation TEXT,
                department TEXT,
                gender TEXT,
                from_date TEXT,
                to_date TEXT,
                is_empty INTEGER DEFAULT 1
            )
        ''')
        
        # Insert sample data for lockers 1-300 if empty
        cursor = conn.execute('SELECT COUNT(*) as count FROM lockers')
        if cursor.fetchone()['count'] == 0:
            for i in range(1, 301):
                conn.execute('INSERT INTO lockers (locker_no) VALUES (?)', (i,))
        conn.commit()

# Login required decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Unauthorized', 'logged_in': False}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('index.html')

@app.route('/login')
def show_login():
    # If already logged in, redirect to home
    if session.get('logged_in'):
        return redirect('/')
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        print(f"Login attempt - Username: {username}")  # Debug log
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()  # Clear any existing session
            session['logged_in'] = True
            session['username'] = username
            session.permanent = True  # Make session permanent (uses PERMANENT_SESSION_LIFETIME)
            
            print("Login successful")  # Debug log
            return jsonify({'success': True, 'message': 'Login successful'})
        
        print("Invalid credentials")  # Debug log
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    is_logged_in = session.get('logged_in', False)
    print(f"Auth check - Logged in: {is_logged_in}")  # Debug log
    return jsonify({'logged_in': is_logged_in})

@app.route('/api/lockers', methods=['GET'])
@login_required
def get_lockers():
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    with get_db() as conn:
        query = 'SELECT * FROM lockers WHERE 1=1'
        params = []
        
        if search:
            query += ''' AND (
                CAST(locker_no AS TEXT) LIKE ? OR
                gc_no LIKE ? OR
                emp_no LIKE ? OR
                name LIKE ? OR
                designation LIKE ? OR
                department LIKE ?
            )'''
            search_param = f'%{search}%'
            params.extend([search_param] * 6)
        
        if status == 'occupied':
            query += ' AND is_empty = 0'
        elif status == 'empty':
            query += ' AND is_empty = 1'
        
        query += ' ORDER BY locker_no'
        
        cursor = conn.execute(query, params)
        lockers = [dict(row) for row in cursor.fetchall()]
    
    return jsonify(lockers)

@app.route('/api/lockers/<int:locker_no>', methods=['GET'])
@login_required
def get_locker(locker_no):
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM lockers WHERE locker_no = ?', (locker_no,))
        locker = cursor.fetchone()
        if locker:
            return jsonify(dict(locker))
        return jsonify({'error': 'Locker not found'}), 404

@app.route('/api/lockers/<int:locker_no>', methods=['PUT'])
@login_required
def update_locker(locker_no):
    data = request.json
    
    with get_db() as conn:
        conn.execute('''
            UPDATE lockers SET
                gc_no = ?,
                emp_no = ?,
                name = ?,
                designation = ?,
                department = ?,
                gender = ?,
                from_date = ?,
                to_date = ?,
                is_empty = ?
            WHERE locker_no = ?
        ''', (
            data.get('gc_no', ''),
            data.get('emp_no', ''),
            data.get('name', ''),
            data.get('designation', ''),
            data.get('department', ''),
            data.get('gender', ''),
            data.get('from_date', ''),
            data.get('to_date', ''),
            0 if data.get('name') else 1,
            locker_no
        ))
        conn.commit()
    
    return jsonify({'success': True})

@app.route('/api/lockers/<int:locker_no>', methods=['DELETE'])
@login_required
def clear_locker(locker_no):
    with get_db() as conn:
        conn.execute('''
            UPDATE lockers SET
                gc_no = NULL,
                emp_no = NULL,
                name = NULL,
                designation = NULL,
                department = NULL,
                gender = NULL,
                from_date = NULL,
                to_date = NULL,
                is_empty = 1
            WHERE locker_no = ?
        ''', (locker_no,))
        conn.commit()
    
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN is_empty = 0 THEN 1 ELSE 0 END) as occupied,
                SUM(CASE WHEN is_empty = 1 THEN 1 ELSE 0 END) as empty
            FROM lockers
        ''')
        stats = dict(cursor.fetchone())
    
    return jsonify(stats)

@app.route('/api/import-excel', methods=['POST'])
@login_required
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload .xlsx or .xls'}), 400
    
    try:
        # Read Excel file
        df = pd.read_excel(file)
        
        # Expected columns
        required_columns = ['locker_no', 'gc_no', 'emp_no', 'name', 'designation', 
                          'department', 'gender', 'from_date', 'to_date']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing columns: {", ".join(missing_columns)}'}), 400
        
        # Import data
        with get_db() as conn:
            imported = 0
            for _, row in df.iterrows():
                locker_no = int(row['locker_no'])
                if 1 <= locker_no <= 300:
                    is_empty = 1 if pd.isna(row['name']) or row['name'] == '' else 0
                    conn.execute('''
                        UPDATE lockers SET
                            gc_no = ?,
                            emp_no = ?,
                            name = ?,
                            designation = ?,
                            department = ?,
                            gender = ?,
                            from_date = ?,
                            to_date = ?,
                            is_empty = ?
                        WHERE locker_no = ?
                    ''', (
                        str(row['gc_no']) if not pd.isna(row['gc_no']) else '',
                        str(row['emp_no']) if not pd.isna(row['emp_no']) else '',
                        str(row['name']) if not pd.isna(row['name']) else '',
                        str(row['designation']) if not pd.isna(row['designation']) else '',
                        str(row['department']) if not pd.isna(row['department']) else '',
                        str(row['gender']) if not pd.isna(row['gender']) else '',
                        str(row['from_date']) if not pd.isna(row['from_date']) else '',
                        str(row['to_date']) if not pd.isna(row['to_date']) else '',
                        is_empty,
                        locker_no
                    ))
                    imported += 1
            conn.commit()
        
        return jsonify({'success': True, 'imported': imported})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-excel', methods=['GET'])
@login_required
def export_excel():
    try:
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM lockers ORDER BY locker_no')
            lockers = [dict(row) for row in cursor.fetchall()]
        
        # Create DataFrame
        df = pd.DataFrame(lockers)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Lockers')
        
        output.seek(0)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'lockers_export_{timestamp}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("🔐 Locker Management System Starting...")
    print("=" * 60)
    print(f"Server running on: http://localhost:5000")
    print(f"Local network access: http://192.168.29.192:5000")
    print(f"\nDefault Login Credentials:")
    print(f"  Username: {ADMIN_USERNAME}")
    print(f"  Password: {ADMIN_PASSWORD}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
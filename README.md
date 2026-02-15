# Flask Web Application on AWS EC2

A full-stack web application built with Python Flask, deployed on Amazon EC2, using Apache with mod_wsgi and SQLite3 as the database.

---

## 🌐 Live URL

```
http://ec2-54-152-142-147.compute-1.amazonaws.com
```

---

## 📋 Assignment Overview

This project implements an interactive multi-page web application that allows users to:

- Register with a username and password
- Submit personal details (name, email, address)
- Upload a text file (Limerick.txt) and view its word count
- Login to retrieve their stored information
- Download the uploaded file

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Cloud Provider | Amazon Web Services (AWS) |
| Server | EC2 t2.micro — Ubuntu Server 24.04 LTS |
| Web Server | Apache 2.4 + mod_wsgi |
| Backend | Python 3 / Flask |
| Database | SQLite3 |
| Frontend | HTML5 / CSS3 |

---

## 📁 Project Structure

```
flaskapp/
├── flaskapp.py          # Main Flask application
├── flaskapp.wsgi        # WSGI entry point for Apache
├── users.db             # SQLite3 database (auto-created)
├── templates/
│   ├── register.html    # Registration page
│   ├── profile.html     # Profile/display page
│   └── login.html       # Login page
├── uploads/             # Stores uploaded text files
└── static/              # Static assets (CSS, images)
```

---

## 🚀 Features

### 1. Registration Page (`/`)
- Accepts username and password
- Accepts first name, last name, email, and address
- Optional file upload (Limerick.txt)
- Stores all data in SQLite3 database
- Redirects to profile page on success

### 2. Profile / Display Page (`/profile/<username>`)
- Displays all submitted user information
- Shows word count from uploaded Limerick.txt
- Provides a download button for the uploaded file

### 3. Login Page (`/login`)
- Accepts username and password
- Validates credentials against the database
- Redirects to profile page on success
- Shows error message on invalid credentials

### 4. File Download (`/download/<username>`)
- Retrieves stored file content from database
- Returns file as a downloadable attachment

---

## ⚙️ AWS EC2 Setup

### Instance Configuration
- **AMI:** Ubuntu Server 24.04 LTS (HVM), SSD Volume Type
- **Instance Type:** t2.micro (Free Tier eligible)
- **Region:** us-east-1 (N. Virginia)
- **Storage:** 8 GB gp3

### Security Group Rules
| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | 0.0.0.0/0 |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

---

## 🔧 Installation & Deployment

### 1. Update System & Install Dependencies
```bash
sudo apt-get update
sudo apt-get install apache2 -y
sudo apt install libapache2-mod-wsgi-py3 -y
sudo apt install python3-pip -y
sudo apt install python3-flask -y
sqlite3 --version
chmod 755 /home/ubuntu/
```

### 2. Create Project Directory
```bash
cd /home/ubuntu
mkdir flaskapp && cd flaskapp
mkdir templates uploads static
```

### 3. Configure Apache
Create `/etc/apache2/sites-available/flaskapp.conf`:
```apache
<VirtualHost *:80>
    WSGIDaemonProcess flaskapp threads=5
    WSGIScriptAlias / /home/ubuntu/flaskapp/flaskapp.wsgi

    <Directory /home/ubuntu/flaskapp>
        WSGIProcessGroup flaskapp
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

    Alias /static /home/ubuntu/flaskapp/static
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### 4. Enable Site & Restart Apache
```bash
sudo a2ensite flaskapp.conf
sudo a2dissite 000-default.conf
sudo chown -R www-data:www-data /home/ubuntu/flaskapp
sudo service apache2 restart
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL UNIQUE,
    password  TEXT NOT NULL,
    firstname TEXT,
    lastname  TEXT,
    email     TEXT,
    address   TEXT,
    limerick  TEXT
);
```

---

## 📄 Application Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Registration page |
| `/register` | POST | Handle registration form |
| `/profile/<username>` | GET | Display user profile |
| `/login` | GET | Login page |
| `/login` | POST | Handle login form |
| `/download/<username>` | GET | Download uploaded file |

---

## 🔍 Troubleshooting

```bash
# View Apache error logs
tail -f /var/log/apache2/error.log

# Test Apache configuration
sudo apache2ctl configtest

# Restart Apache
sudo service apache2 restart

# Fix permissions
sudo chown -R www-data:www-data /home/ubuntu/flaskapp
sudo chmod 755 /home/ubuntu/
```

---

## ⚠️ Known Notes

- Passwords are stored in plain text (acceptable for this academic assignment; use hashing like `bcrypt` in production)
- The app uses `http://` only — SSL/HTTPS not configured for this assignment
- Public IP changes on EC2 stop/start unless an Elastic IP is assigned

---

## 👤 Author

**Vidit Parekh**  
AWS EC2 Flask Web Application Assignment

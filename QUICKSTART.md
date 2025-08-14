# Quick Start Guide

Get PubManager running in 5 minutes!

## 🚀 Super Quick Setup

### 1. Create Virtual Environment
```bash
python -m venv myworld
```

### 2. Activate Virtual Environment
**Windows (Git Bash):**
```bash
source myworld/Scripts/activate
```

**Windows (Command Prompt):**
```bash
myworld\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source myworld/bin/activate
```

### 3. Update Database Settings
Edit the `.env` file with your MySQL credentials:
```bash
DB_NAME=pubmanager_db
DB_USER=your_username
DB_PASSWORD=your_password
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```

### 6. Start the Server
```bash
python manage.py runserver
```

### 7. Open Your Browser
Go to: `http://127.0.0.1:8000/`

## 🎯 What You Get

- **Staff Management**: Add/edit/delete staff members
- **Role Management**: Manage staff roles and permissions  
- **Task Management**: Create and assign tasks with deadlines
- **Calendar View**: Visual task calendar interface
- **User Authentication**: Login/logout system

## ⚠️ Prerequisites

- Python 3.8+
- MySQL Server
- Git (for cloning)

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed instructions
- Look at the [Troubleshooting](README.md#troubleshooting) section
- Ensure your virtual environment is activated (you should see `(myworld)` in your terminal)

## 🔧 Customization

After getting it running, you can:
- Modify models in `pub/models.py`
- Add new views in `pub/views.py`
- Customize templates in `pub/templates/`
- Update URLs in `pub/urls.py`

Happy coding! 🎉

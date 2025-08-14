# PubManager - Django Project

A Django-based publication management system for managing staff, roles, and tasks.

## Prerequisites

Before installing this project, make sure you have the following installed on your system:

- **Python 3.8+** (recommended: Python 3.11 or 3.12)
- **MySQL Server** (version 5.7+ or 8.0+)
- **Git** (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd pubmanager
```

### 2. Create a Virtual Environment

**Windows (Git Bash):**
```bash
python -m venv myworld
source myworld/Scripts/activate
```

**Windows (Command Prompt):**
```bash
python -m venv myworld
myworld\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
python -m venv myworld
myworld\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv myworld
source myworld/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE pubmanager_db;
   ```

2. **Configure Database Connection:**
   
   Create a `.env` file in the project root:
   ```bash
   # Database Configuration
   DB_NAME=pubmanager_db
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   
   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **Update settings.py:**
   
   The project is configured to use environment variables. Make sure your `.env` file is properly set up.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
pubmanager/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (create this)
├── pubmanager/              # Project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── pub/                     # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL configuration
│   ├── admin.py             # Admin interface
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
└── myworld/                 # Virtual environment
```

## Features

- **Staff Management**: Add, edit, and delete staff members
- **Role Management**: Manage staff roles and permissions
- **Task Management**: Create and assign tasks with deadlines
- **Calendar View**: Visual task calendar interface
- **User Authentication**: Login/logout system

## Configuration

### Environment Variables

The following environment variables can be configured in your `.env` file:

- `DB_NAME`: MySQL database name
- `DB_USER`: MySQL username
- `DB_PASSWORD`: MySQL password
- `DB_HOST`: MySQL host (default: localhost)
- `DB_PORT`: MySQL port (default: 3306)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Configuration

The project is configured to use MySQL. If you need to use a different database:

1. Update the database engine in `settings.py`
2. Install the appropriate database adapter
3. Update the `requirements.txt` file

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'mysqlclient'**
   - Install MySQL development libraries
   - On Windows: Download and install MySQL Connector/C
   - On Ubuntu/Debian: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

2. **Database Connection Error**
   - Verify MySQL server is running
   - Check database credentials in `.env` file
   - Ensure database exists

3. **Port Already in Use**
   - Change the port: `python manage.py runserver 8001`
   - Or kill the process using the port

### Getting Help

If you encounter issues:

1. Check the Django error logs
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Check database connection settings

## Development

### Adding New Features

1. Create new models in `pub/models.py`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Add views in `pub/views.py`
4. Update URL configuration in `pub/urls.py`
5. Create templates in `pub/templates/`

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic

## Deployment

### Production Considerations

1. **Security:**
   - Set `DEBUG=False` in production
   - Use strong, unique `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` properly
   - Use HTTPS

2. **Database:**
   - Use production-grade MySQL server
   - Regular backups
   - Optimize database queries

3. **Static Files:**
   - Run `python manage.py collectstatic`
   - Serve static files through web server (nginx, Apache)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support contact information here]

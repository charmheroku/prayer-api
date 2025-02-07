# 👨‍👩‍👧‍👦 Prayer-Api

Django application that unites people in their good deeds.
Service for creating prayer groups, publishing prayers, joining a community and supporting each other.

## Main idea
This project allows you to:

- Register and authorize users (administrators, ordinary participants)
- Create and manage prayer groups (public and private)
- Publish prayers in certain categories
- Pray together for common or personal needs
- Send requests to join private groups

## 🌐 Try the API with Swagger Online

You can explore the project live: [Prayer API]([https://prayer-api-z92x.onrender.com/api/schema/swagger/])  

### Test Admin Credentials:  
- **Email**: `admin@example.com`  
- **Password**: `admin12345`  

Feel free to log in and explore the features!

## Main functional blocks

1. **User management**  

   - Registration and login to the system  
   - User profile (avatar, detailed information)  
   - Roles and rights (admin, user)

2. **Prayers and categories**  
   - Create and edit prayers  
   - Categories (for example, “World in Ukraine”, “Defenders”, “Healing”, “Thanksgiving”)  
   - Division by levels of privacy (public, group, private)


3. **Groups and membership**  
   - Create public and private communities  
   - Managing participants (admin, participant)  
   - Sending and approving requests to join closed groups

4. **Prayer requests**  
   - Ability to create prayer requests  
   - Count of prayers (prayer_count) and support  
   - Comments system (if needed)

5. **Administration**  
   - Convenient panel for admin (through Django Admin)  
   - Content configuration and moderation

## Technologies and tools

- **Python 3.11** and **Django 4.x**  
- **PostgreSQL** (or another relational database)  
- **Docker** / **docker-compose** for containerization  
- **pip-tools** for managing dependencies  
- **Whitenoise** for serving static files in production  

- **Gunicorn** or **uWSGI** for running the application  
- **Nginx** (recommended for a production server)  
- **DRF Spectacular** for documentation (Swagger / Redoc)

## Project structure

- **apps/users**  
  Models, serializers and views for managing users.  
  
- **apps/prayer**  
  Models and functionality for publishing prayers, categories, groups and membership.

- **config**  
  - **settings**: base settings from `base.py`, as well as environments `dev.py`, `prod.py`  
  - **urls.py**: main routes  
  - **wsgi.py**: entry point for WSGI servers (gunicorn, uWSGI)  

- **fixtures**  
  Directory for JSON files with test data.

- **requirements**  
  Subdirectories `base.in`, `local.in`, `production.in` and final compiled `.txt`:
  - `pip-compile requirements/base.in`
  - `pip-sync requirements/base.txt`

## Quick start (locally)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_org_or_username/prayer-platform.git
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements/local.txt
   ```
3. **Run migrations**:
   ```bash
   python manage.py migrate

   ```

4. **Load fixtures** (if you want):
   ```bash
   python manage.py loaddata fixtures/initial_data.json
   ```


5. **Run the server**:
   ```bash
   python manage.py runserver

   ```
   The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

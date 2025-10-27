# book_website_backend

Prerequisites
- Python 3.10+
- pip

Steps to run
1. Go to the backend folder:
```bash
cd backend
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` based on `.env.example` and fill in at minimum:
- DJANGO_SECRET_KEY
- DEBUG
- DATABASE_URL
- CORS_ALLOWED_ORIGINS
- JWT/ACCESS/REFRESH settings (if needed)
5. Apply migrations:
```bash
python manage.py migrate
```
6. Create a superuser:
```bash
python manage.py createsuperuser
```
7. Run the server:
```bash
python manage.py runserver
```
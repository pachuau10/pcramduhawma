# PC Ramduhawma's Homepage

A nostalgic early-internet / late-1990s / early-2000s personal homepage built with Django.

## Features

- Dynamic blog posts
- Software downloads with file upload
- Projects showcase
- Photo gallery
- Guestbook with spam protection
- Visitor counter
- Site search
- Django admin management
- Responsive retro design
- Cloudinary image storage
- Neon PostgreSQL support

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

### 3. Database

For local development (SQLite):

```bash
python manage.py migrate
python manage.py loaddata core/fixtures/initial_data.json
```

For production (Neon PostgreSQL):

```bash
set DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
python manage.py migrate
python manage.py loaddata core/fixtures/initial_data.json
```

### 4. Cloudinary (Optional)

Set environment variables:

```bash
set CLOUDINARY_CLOUD_NAME=your-cloud-name
set CLOUDINARY_API_KEY=your-api-key
set CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
pcramduhawma/
├── config/          # Django project settings
├── core/            # Site settings, visitor counter, navigation
├── blog/            # Blog posts with categories and tags
├── software/        # Software downloads with file uploads
├── projects/        # Projects showcase
├── gallery/         # Photo gallery
├── guestbook/       # Guestbook with moderation
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── media/           # User uploads
```

## Deployment

### Production Checklist

1. Set `DEBUG=False`
2. Set `SECRET_KEY` environment variable
3. Set `ALLOWED_HOSTS`
4. Set `DATABASE_URL` for Neon PostgreSQL
5. Set Cloudinary credentials
6. Run `python manage.py collectstatic`
7. Use Gunicorn: `gunicorn config.wsgi:application`

### Example Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## License

All rights reserved.

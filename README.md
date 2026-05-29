# BlogProfile - Modern Django Blog

A full-featured, modern blog website built with Django and SQLite, featuring a beautiful frontend and custom admin dashboard.

## Features

### Public Website
- Modern, responsive design with beautiful UI
- Blog post listing with pagination
- Blog post detail page with comments and likes
- Category and tag filtering
- Full-text search
- Featured posts section
- About page
- Contact form
- SEO-friendly URLs
- Social media links in footer
- Mobile, tablet, and desktop responsive

### Admin Dashboard
- Custom admin panel (not just Django default)
- Dashboard overview with statistics cards
- Blog post CRUD (Create, Read, Update, Delete)
- Category management
- Tag management
- Comment moderation (approve/delete)
- Contact message inbox
- Publish/draft post status
- Modern sidebar navigation
- Responsive admin layout

## Tech Stack

- **Backend:** Django 5.1
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** HTML5, CSS3, JavaScript
- **CSS:** Custom design system with CSS variables, gradients, shadows
- **Icons:** Font Awesome 6
- **Fonts:** Google Fonts (Inter)
- **Deployment:** Render

## Project Structure

```
blogprofile/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── runtime.txt           # Python version for Render
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── project/              # Django project settings
│   ├── __init__.py
│   ├── settings.py       # Main settings
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI for deployment
│   └── asgi.py           # ASGI config
├── blog/                 # Blog application
│   ├── __init__.py
│   ├── admin.py          # Django admin registration
│   ├── apps.py           # App configuration
│   ├── models.py         # Database models
│   ├── views.py          # Views (public + dashboard)
│   ├── urls.py           # URL routes
│   ├── forms.py          # Form definitions
│   ├── decorators.py     # Custom decorators
│   ├── context_processors.py  # Template context
│   └── migrations/
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── blog/             # Public blog templates
│   │   ├── index.html
│   │   ├── post_detail.html
│   │   ├── category.html
│   │   ├── tag.html
│   │   ├── search.html
│   │   ├── about.html
│   │   └── contact.html
│   └── dashboard/        # Admin panel templates
│       ├── base.html
│       ├── login.html
│       ├── index.html
│       ├── posts.html
│       ├── post_form.html
│       ├── post_confirm_delete.html
│       ├── categories.html
│       ├── tags.html
│       ├── comments.html
│       └── messages.html
├── static/               # Static files
│   ├── css/
│   │   ├── style.css     # Public site styles
│   │   └── dashboard.css # Admin panel styles
│   ├── js/
│   │   └── main.js       # JavaScript
│   └── images/
└── media/                # User uploaded files
```

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blogprofile.git
   cd blogprofile
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the website**
   - Website: http://127.0.0.1:8000/
   - Admin Dashboard: http://127.0.0.1:8000/dashboard/
   - Django Admin: http://127.0.0.1:8000/admin/

## Creating Sample Content

1. Login to the admin dashboard at `/dashboard/`
2. Create categories (e.g., Technology, Design, Lifestyle)
3. Create tags (e.g., Python, Django, Web)
4. Create blog posts with featured images

## Deployment to Render

### Prerequisites
- GitHub account
- Render account

### Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/blogprofile.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** blogprofile
     - **Environment:** Python
     - **Build Command:**
       ```
       pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
       ```
     - **Start Command:**
       ```
       gunicorn project.wsgi:application
       ```
   - Add environment variables:
     - `SECRET_KEY`: Generate a Django secret key
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `.onrender.com,127.0.0.1,localhost`
     - `DATABASE_URL`: (Optional for PostgreSQL)
   - Click "Create Web Service"

3. **Create Superuser on Render**
   ```bash
   # Use Render Shell or run:
   python manage.py createsuperuser
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes (production) |
| `DEBUG` | Debug mode (True/False) | Yes |
| `ALLOWED_HOSTS` | Comma-separated hosts | Yes |
| `DATABASE_URL` | Database URL (for PostgreSQL) | Optional |

## Screenshots

*[Add screenshots here]*

## License

MIT License

## Author

Your Name

---

Made with ❤️ and Django

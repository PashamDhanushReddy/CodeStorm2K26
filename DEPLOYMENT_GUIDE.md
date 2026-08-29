# Deployment Configuration Guide for Render

## Environment Variables Required for Production

Add these to your Render dashboard under Environment Variables:

### Required Variables:
```
SECRET_KEY=your-secret-key-here
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com
```

### Optional Variables:
```
DEBUG=False
DATABASE_URL=your-postgres-database-url-if-using-render-postgres
```

## Build Command for Render:
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

## Start Command for Render:
```bash
gunicorn codestorm_project.wsgi:application
```

## Important Notes:

1. **Database**: The registration form is automatically connected to your PostgreSQL (Neon) database. Ensure the connection URL is provided in the `DATABASE_URL` environment variable.

2. **File Uploads**: The PPT handling has been set up to use Cloudinary.
   
3. **Static Files**: WhiteNoise is configured to serve static files automatically

5. **Environment Variables**: Make sure all variables are set before deploying

6. **CSRF Configuration**: The app now includes proper CSRF settings for production deployment

## CSRF Configuration Added:

The application now includes:
- `CSRF_COOKIE_SECURE = True` for production (uses HTTPS cookies)
- `CSRF_TRUSTED_ORIGINS` automatically configured with your Render hostname
- Session security settings for production environments

## Testing Locally:
```bash
# Test with production-like settings
export DEBUG=False
export SECRET_KEY=your-secret-key
python manage.py runserver
```

## Troubleshooting:

- **CSRF Verification Failed**: Make sure your `RENDER_EXTERNAL_HOSTNAME` is set correctly in Render
- If `collectstatic` fails, make sure `whitenoise` is in your requirements.txt
- If the database connection fails, check your `DATABASE_URL`
- If the registration form doesn't load, check that all required environment variables are set
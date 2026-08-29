# Deployment Configuration Guide for Render

## Environment Variables Required for Production

Add these to your Render dashboard under Environment Variables:

### Required Variables:
```
SECRET_KEY=your-secret-key-here
SUPABASE_URL=https://divhwqupyptmuotlzqpn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpdmh3cXVweXB0bXVvdGx6cXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY3NjMxNDIsImV4cCI6MjA4MjMzOTE0Mn0.byZcoPz1SG6olNX_x17jKoqyVwuUKhPeO_JnDauR4A4
SUPABASE_BUCKET_NAME=codestorm-ppt
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

1. **Supabase Table Structure**: The registration form now matches your exact table structure with:
   - Team details: `team_name`, `college`, `branch`, `year_of_study`
   - Idea details: `idea_title`, `idea_theme` (not `idea_description` or `idea_track`)
   - PPT uploads: `ppt_file_path` (required field)
   - YouTube link: `youtube_link` (optional field)
   - Member details: `member1-6` with `name`, `email`, `phone`, `roll`, and `is_leader` fields

2. **Supabase Bucket**: If you want PPT uploads to work, create the `codestorm-ppt` bucket in your Supabase dashboard

3. **Database**: The registration system will work with your existing Supabase table with exact column mapping

4. **Static Files**: WhiteNoise is configured to serve static files automatically

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
- If Supabase connection fails, check your URL and key in the environment variables
- If the registration form doesn't load, check that all required environment variables are set
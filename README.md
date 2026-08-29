# CodeStorm 2026 Website

This is the official website for CodeStorm 2026, built with Django.

## Local Development

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Run server:**
    ```bash
    python manage.py runserver
    ```

## Deployment on Render

This project is configured for easy deployment on Render.

1.  Push this code to a GitHub/GitLab repository.
2.  Log in to [Render](https://render.com/).
3.  Click "New +" -> "Blueprint".
4.  Connect your repository.
5.  Render will automatically detect `render.yaml` and set up the Web Service (Django) and the Database (PostgreSQL).
6.  Approve the deployment.

Alternatively, you can manually create a Web Service:
-   **Build Command:** `./build.sh`
-   **Start Command:** `gunicorn codestorm_project.wsgi:application`
-   Add Environment Variable `DATABASE_URL` (Internal Connection String of your Postgres DB).
-   Add Environment Variable `SECRET_KEY`.

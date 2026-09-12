# Deploy to Render with Neon

This project uses SQLite locally and automatically uses PostgreSQL when the
`DATABASE_URL` environment variable is present. Do not use SQLite in production:
Render's local filesystem is temporary.

## 1. Put the project on GitHub

Create a new GitHub repository and push this project to it. Do not commit `.env`,
`db.sqlite3`, `media/`, or `staticfiles/`.

## 2. Create the database in Neon

1. Create a free Neon account at <https://neon.tech>.
2. Create a project and select PostgreSQL.
3. From the **Connect** panel, copy the connection string. It starts with
   `postgresql://`.

## 3. Create the Render web service

1. Open <https://dashboard.render.com> and sign in with GitHub.
2. Select **New** > **Blueprint** and select your repository. Render reads
   `render.yaml` and fills in the build and start commands.
3. Before creating the service, add these environment variables:

   - `DATABASE_URL`: paste the Neon connection string.
   - `DJANGO_ADMIN_USERNAME`: your desired admin username, for example `caleb`.
   - `DJANGO_ADMIN_EMAIL`: your admin email address.
   - `DJANGO_ADMIN_PASSWORD`: a long, unique password.

4. Create the Blueprint and wait for the deployment to finish.

Render runs the following during every deployment:

```text
./build.sh
```

That installs dependencies, collects static files, and applies Django migrations.

## 4. Sign in to Django admin

The first deployment creates the administrator from the three `DJANGO_ADMIN_*`
variables above. It safely skips creation on future deployments. Sign in at
`https://YOUR-SERVICE.onrender.com/admin/`.

After you have confirmed that the account works, delete `DJANGO_ADMIN_PASSWORD`
from Render and redeploy. The account remains in Neon; the password is not
needed after it has been created.

## Important free-tier limits

- The Render web service sleeps after 15 minutes without visitors. The first
  request after that can take about a minute.
- Neon keeps the database persistent, but its free-plan usage allowance applies.
- Images that are already in `portfolio/static/` deploy normally. Files uploaded
  through the Django admin go to `media/` and will be lost when Render restarts.
  Use Cloudinary or another object-storage service before relying on uploads.

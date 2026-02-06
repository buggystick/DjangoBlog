# BlogSite

A Django 5.x blog site with S3-backed storage (RustFS).

## Features
- Public blog posts with admin editing.
- Private media uploads for cover images (served via presigned URLs).
- Static assets served from public-read S3 bucket.
- Production-ready Dockerfile for containerization.

## Architecture & Storage
- **RustFS S3 API**: Used for both static and media storage.
- **Static Files**: Stored in `blog-static` bucket under `static/` prefix. Configured for public-read access.
- **Media Files**: Stored in `blog-media` bucket (private). Accessed via a Django view that generates a 302 redirect to a presigned S3 GET URL.

## Local Development
1. Clone the repository.
2. Create a `.env` file with the following variables:
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_S3_ENDPOINT_URL=https://rustfs.dsreed.net/api/
   STATIC_BUCKET=blog-static
   MEDIA_BUCKET=blog-media
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start development server:
   ```bash
   python manage.py runserver
   ```

## Docker
You can build the production image using the provided Dockerfile:
```bash
docker build -t blogsite:latest -f docker/Dockerfile .
```

## Creating Admin User
```bash
python manage.py createsuperuser
```

## Bucket Policy Expectations
- **blog-static**: Should allow anonymous `s3:GetObject` for the `static/*` prefix.
- **blog-media**: Should deny anonymous access; only signed requests from Django (using AWS credentials) succeed.

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
RUN pip install --no-cache-dir "django>=5.1,<5.2" "django-storages[s3]" "boto3" "psycopg[binary]" "gunicorn" "python-dotenv" "dj-database-url" "Pillow"

COPY . /app/

RUN mkdir -p /app/staticfiles /app/media

RUN addgroup --system django && adduser --system --group django
RUN chown -R django:django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "blogsite.wsgi:application"]

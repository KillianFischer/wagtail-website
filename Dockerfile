# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    NODE_VERSION=20

# Set work directory
WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update --yes --quiet && \
    apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install and build Tailwind CSS
WORKDIR /app/theme/static_src
RUN npm install
RUN npm run build
RUN npm run dev

# Back to app directory
WORKDIR /app

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=mysite.settings.base exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8080 --workers 4 --timeout 120"]
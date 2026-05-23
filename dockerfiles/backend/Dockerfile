FROM python:3.13-alpine

RUN apk add --no-cache nodejs npm

WORKDIR /app

# Install Python dependencies
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY web/ .

# Build CSS and collect static files
RUN npm install \
    && npx sass studyflow/src/sass/main.scss studyflow/static/css/main.css \
        --no-source-map --style=compressed \
    && rm -rf node_modules \
    && DJANGO_SETTINGS_MODULE=studyflow.settings \
       SECRET_KEY=placeholder \
       POSTGRES_HOST=placeholder \
       python manage.py collectstatic --noinput

COPY web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

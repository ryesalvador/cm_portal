# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /mysite

# Install dependencies
RUN pip install --upgrade pip
RUN pip install cm-portal 

# Copy project
#COPY . /code/
RUN django-admin.py startproject mysite .
RUN echo "INSTALLED_APPS += ['cm_portal.apps.CmPortalConfig', 'sortedm2m',]" >> mysite/settings.py
RUN echo "STATIC_ROOT = os.path.join(BASE_DIR, 'static')" >> mysite/settings.py
RUN echo "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')" >> mysite/settings.py
RUN echo "MEDIA_URL = '/media/'" >> mysite/settings.py
RUN echo "LOGIN_REDIRECT_URL = '/'" >> mysite/settings.py
RUN echo "from django.conf.urls import include" >> mysite/urls.py
RUN echo "urlpatterns += [path('', include('cm_portal.urls')), path('accounts/', include('django.contrib.auth.urls')),]" >> mysite/urls.py
RUN python manage.py migrate
RUN python manage.py migrate cm_portal

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Camillus MedHaven Portal: A Django Web App for a Nursing Home Facility

## Installation
1. Add cm_portal and its dependency to your `INSTALLED_APPS` like this:
~~~~
    INSTALLED_APPS = [    
        ...
        'cm_portal.apps.CmPortalConfig',
        ...
    ] 
~~~~

2. Append the following environment variables to your `settings.py`.
    ~~~~
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    LOGIN_REDIRECT_URL = '/'
    ~~~~

3. Include the cm_portal URLconf in your project `urls.py` like this:
~~~~
    from django.conf.urls import include
    urlpatterns += [
        path('', include('cm_portal.urls')),
    ]

    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
    ]
 ~~~~

4. Run `python manage.py migrate` to create the cm_portal models.

5. Start the development server and visit http://127.0.0.1:8000/
   to begin using app.

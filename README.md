# Camillus MedHaven Portal: A Django Web App for a Nursing Home Facility

## Requirements
This web app requires Python 3. It is recommended to test it on `virtualenv` first. So on `virtualenv` you do:
    `$ virtualenv .venv -p /usr/bin/python3`
    `$ source .venv/bin/activate`

## Installation
1. Add cm_portal and its dependency to your `INSTALLED_APPS` like this:
~~~~
    INSTALLED_APPS = [    
        ...
        'cm_portal.apps.CmPortalConfig',
        'sortedm2m',
        ...
    ] 
~~~~

2. Include the cm_portal URLconf in your project urls.py like this::
~~~~
    from django.conf.urls import include
    urlpatterns += [
        path('', include('cm_portal.urls')),
    ]

    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
    ]
 ~~~~

3. Run `python manage.py migrate` to create the cm_portal models.

4. Start the development server and visit http://127.0.0.1:8000/
   to begin using app.

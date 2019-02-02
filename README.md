# Camillus MedHaven Portal: A Django Web App for a Nursing Home Facility

## Requirements
This web app requires Python 3. It is recommended to test it on `virtualenv` first. So on `virtualenv` you do:
    `$ virtualenv .venv -p /usr/bin/python3`
    `$ source .venv/bin/activate`

## Installation
1. Install latest version of Django.
    `$ pip install django`

2. Create a project and download source.
    `$ django-admin startproject mysite`
    `$ cd mysite`
    `$ git clone https://gitlab.com/salvadorrye/cm_portal.git`

3. Install requirements.
    `$ cd cm_portal`
    `$ pip install -r requirements.txt`
    `$ cd ..`

4. Then open the `settings.py` of your project and include the following to your `INSTALLED_APPS`:
    ~~~~
    INSTALLED_APPS = [    
        ...
        'cm_portal.apps.CmPortalConfig',
        'django_dropbox_storage',
        'django_cleanup',
        'sortedm2m',
        ...
    ] 
    ~~~~

5. Append the following environment variables to your `settings.py` and fill in `'xxx'` with corresponding credentials (If you don't have `DROPBOX_ACCESS_TOKEN` you can create one after creating a Dropbox app at [Dropbox for Developers](https://www.dropbox.com/developers)).
    ~~~~
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    LOGIN_REDIRECT_URL = '/'

    DROPBOX_ACCESS_TOKEN = 'xxx'
    DROPBOX_ACCESS_TOKEN_SECRET = 'xxx'
    DROPBOX_CONSUMER_KEY = 'xxx'
    DROPBOX_CONSUMER_SECRET = 'xxx'
    ~~~~

6. Open your `urls.py` and append the following.
    ~~~~
    from django.conf.urls import include
    urlpatterns += [
        path('', include('cm_portal.urls')),
    ]

    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
    ]
    ~~~~

7. Apply migrations.
    `$ ./manage migrate`

8. Test run server.
    `$ ./manage runserver`

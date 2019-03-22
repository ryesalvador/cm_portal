import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requires = [
    "django",
    "Pillow",
]

setup(
    name='cm_portal',
    version='0.0.4444',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',  
    description='A Django Web App for a Nursing Home Facility',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ryesalvador/cm_portal/',
    author='Rye Salvador',
    author_email='salvadorrye@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=requires,
)

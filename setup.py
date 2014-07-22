from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name='pubbot',
    version=version,
    author='John Carr',
    author_email='john.carr@unrouted.co.uk',
    license='Apache Software License',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django',
        'dj-database-url',
        'psycopg2',
        'South',
        'django-zap',
        'gevent',
        'greenlet',
        'gevent-psycopg2',
        'geventirc',
        'gunicorn',
        'requests',
        'beautifulsoup4',
        'django_polymorphic',
        ],
    )


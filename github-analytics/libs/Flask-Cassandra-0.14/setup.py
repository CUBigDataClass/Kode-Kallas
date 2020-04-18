"""
Flask-Cassandra
-------------

Flask-Cassandra provides an application-level connection
to an Apache Cassandra database. This connection can be
used to interact with a Cassandra cluster.

"""
from setuptools import setup


setup(
    name='Flask-Cassandra',
    version='0.14',
    url='http://terbiumlabs.com/flask-cassandra/',
    license='BSD',
    author='Michael Moore',
    author_email='michael@terbiumlabs.com',
    description='Provides a connection to a Cassandra cluster in a Flask app',
    long_description=__doc__,
    py_modules=['flask_cassandra'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'cassandra-driver'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

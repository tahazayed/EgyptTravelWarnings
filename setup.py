from setuptools import setup, find_packages

setup(
    name         = 'egypttravelwarning',
    version      = '1.1',
    packages     = find_packages(),
    install_requires=[
        'pip',
        'distribute',
        'scrapy',
        'psycopg2',
        'bs4',
        'pymongo',
        'pymssql'
    ],
    entry_points = {'scrapy': ['settings = egypttravelwarning.settings']},
    scripts = ['bin/testargs.py']
)
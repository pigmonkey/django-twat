from setuptools import setup, find_packages

setup(
    name = 'django-twat',
    version = '0.1',
    description = 'A simple Django app to pull and display tweets.',
    long_description = open('README.md').read(),
    url = 'https://github.com/pigmonkey/django-twat',
    author = 'Pig Monkey',
    author_email = 'pm@pig-monkey.com',

    packages = find_packages(),
    zip_safe=False,
)

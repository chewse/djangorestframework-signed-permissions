import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangorestframework-signed-permissions',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.4', 'djangorestframework'],
    license='MIT License',  # example license
    description='Allow access to your REST resources via a signed url',
    long_description=README,
    author='Chewse',
    author_email='james@chewse.com',
    url='https://github.com/chewse/djangorestframework-signed-permissions',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)

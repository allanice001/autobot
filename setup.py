from setuptools import setup, find_packages

setup(
    install_requires=[
        'flask',
        'flask_restful',
        'flask_paginate',
        'pyyaml',
        'pymongo',
        'twisted',
        'mako',
    ],
    packages=find_packages(exclude=['tests'])
)
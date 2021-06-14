import os
from setuptools import setup


README_PATH = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README_PATH) as f:
    README_DATA = f.read()


setup(
    name                          = 'lilcache',
    version                       = '0.0.1',
    description                   = 'Inter process and thread safe light weight cache',
    long_description              = README_DATA,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/return007/lilcache',
    author                        = 'return007',
    author_email                  = 'glalchandanig@gmail.com',
    packages                      = ['lilcache'],
    include_package_data          = True,
    python_requires               = '>=2.7',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
    ],
    extras_require={
        'dev': [
            'pytest',
        ]
    }
)

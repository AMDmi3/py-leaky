#!/usr/bin/env python3

from os import path

from setuptools import Extension, setup


def get_long_description():
    try:
        with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as readmedata:
            return readmedata.read()
    except:
        return None


setup(
    name='leaky',
    version='0.0.0',
    description='Test Python module which leaks memory',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Dmitry Marakasov',
    author_email='amdmi3@amdmi3.ru',
    url='https://github.com/AMDmi3/py-leaky',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    ext_modules=[
        Extension(
            'leaky',
            sources=[
		'src/leaky.c',
            ],
        )
    ]
)

"""
Project home:
https://gitlab.com/szuro/zappix
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='zappix',
    version='1.2.3',
    description='A Python replacement for Zabbix sender and get.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/szuro/zappix',
    author='Robert Szulist',
    author_email='r.szulist@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='zabbix get sender agent active',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    test_suite="tests",
    install_requires=[
        "pyOpenSSL",
        "pyopenssl-psk"
    ],
    extras_require={
        'dev': [
            'tox',
            'pyzabbix'
        ]
    }
)

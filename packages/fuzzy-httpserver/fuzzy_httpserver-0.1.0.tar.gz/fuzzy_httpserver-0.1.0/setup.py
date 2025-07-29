from setuptools import setup

setup(
    name='fuzzy-httpserver',
    version='0.1.0',
    description='Fuzzy matching HTTP file server with autocomplete and fallback',
    author='PakCyberbot',
    author_email='pakcyberbot@gmail.com',
    packages=['fuzzy_httpserver'],
    entry_points={
        'console_scripts': [
            'fuzzy-httpserver = fuzzy_httpserver.server:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)

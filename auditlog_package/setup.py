from setuptools import setup, find_packages

setup(
    name='audit-trail-logger',
    version='0.1.3',
    description='A Django package for logging actions with user and object details',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Urvashi Sardare',
    author_email='urvashisardare@gmail.com',
    url='https://github.com/sardareurvashi05/audit-trail-logger',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

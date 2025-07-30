from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='EditableFlask',
    version='2.0.0',
    description='Addon to Flask to edit HTML content in a running app.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/YOUR_USERNAME/EditableFlask',
    author='Mahir Shah',
    author_email='mahir.shah.sd@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='flask editable live edit',
    packages=find_packages(include=['EditableFlask', 'EditableFlask.*']),
    include_package_data=True,
    package_data={
        'EditableFlask': [
            'templates/*.html',
            'templates/*.htm',
            'assets/**/*',
            'pyfiles/*.py'
        ],
    },
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'psutil',
    ]
)

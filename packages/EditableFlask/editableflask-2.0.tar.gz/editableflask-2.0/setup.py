from setuptools import setup, find_packages
from pathlib import Path

# ✅ FIX: force UTF-8 so Windows doesn't default to cp1252
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='EditableFlask',
    version='2.0',
    description='Addon to Library named flask which helps to edit html content in running app0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Mahir Shah',
    author_email='mahir.shah.sd@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='editable_flask',
    packages=find_packages(),
    package_data={
        'EditableFlask': ['templates/*.html', 'assets/**'],
    },
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'psutil'
    ]
)

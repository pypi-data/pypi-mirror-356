from setuptools import setup, find_packages
import os
import glob

setup(
    name="flet_sqlite3",
    version="0.5.0",
    author="Noon",
    author_email="noon@example.com",
    description="Приложение для учета партнеров и расчета скидок с использованием Flet и SQLite3",
    long_description="Приложение для учета партнеров и расчета скидок с использованием Flet и SQLite3",
    long_description_content_type="text/markdown",
    url="https://github.com/noon/flet_sqlite3",
    packages=['flet_sqlite3'],  # Явно указываем пакет
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flet>=0.28.0",
        "openpyxl>=3.1.0",
    ],
    include_package_data=True,
    package_data={
        'flet_sqlite3': ['*.py', '*.ico', '*.xlsx', '*.db'],
    },
) 
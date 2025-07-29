from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("install.me", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="flet_sqlite3",
    version="0.1.0",
    author="Noon",
    author_email="noon@example.com",
    description="Приложение для учета партнеров и расчета скидок с использованием Flet и SQLite3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noon/flet_sqlite3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "flet_sqlite3": ["*.ico", "*.xlsx", "*.db"],
    },
) 
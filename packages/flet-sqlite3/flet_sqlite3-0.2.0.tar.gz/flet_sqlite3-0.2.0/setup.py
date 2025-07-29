from setuptools import setup, find_packages
import os
import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("install.me", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip()]

# Получаем список всех файлов в директории
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if not filename.endswith('.py') and not filename == 'setup.py':
                paths.append(os.path.join('..', path, filename))
    return paths

# Находим все файлы данных
extra_files = package_files('.')

# Добавляем все файлы Excel
excel_files = glob.glob('*.xlsx')
ico_files = glob.glob('*.ico')
db_files = glob.glob('*.db')

# Объединяем все файлы
all_files = extra_files + excel_files + ico_files + db_files

setup(
    name="flet_sqlite3",
    version="0.2.0",
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
        "": all_files,
    },
) 
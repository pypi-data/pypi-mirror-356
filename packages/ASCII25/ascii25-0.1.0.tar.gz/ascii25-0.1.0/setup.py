from setuptools import setup, find_packages

setup(
    name="ASCII25",
    version="0.1.0",
    author="Noon",
    author_email="noon@night-watchers.com",
    description="Простая библиотека для создания ASCII-арта",
    long_description="Библиотека предоставляет инструменты для создания ASCII-арта",
    long_description_content_type="text/markdown",
    url="https://github.com/noon/ASCII",
    packages=['ASCII'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "sqlite3>=3.1.0",
    ],
    include_package_data=True,
    package_data={
        'ASCII': ['*.py'],
    },
) 
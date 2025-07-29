from setuptools import setup, find_packages

setup(
    name="ASCII25",
    version="0.2.2",
    author="Noon",
    author_email="noon@night-watchers.com",
    description="Простая библиотека для создания ASCII-арта",
    long_description="Библиотека предоставляет инструменты для создания ASCII-арта",
    long_description_content_type="text/markdown",
    url="https://github.com/noon/ASCII",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flet",
        "openpyxl",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "scipy",
        "statsmodels",
        "plotly"
    ],
    include_package_data=True,
    package_data={
        'ASCII': ['*.py', 'core/*.pyd', 'core/*', 'utils/*'],
    },
) 
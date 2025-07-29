from setuptools import setup, find_packages

setup(
    name="django_fast",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.2,<5.0",
        "uvicorn>=0.22,<1.0",
    ],
    entry_points={
        "console_scripts": [
            "django-fast = django_fast.cli:main",  # adjust name/module path
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    python_requires=">=3.8",
)

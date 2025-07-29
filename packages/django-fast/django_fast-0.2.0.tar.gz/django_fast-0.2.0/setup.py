from setuptools import setup, find_packages

setup(
    name="django-fast",
    version="0.2.0",
    description="A fast Django-like microframework",
    author="Your Name",
    author_email="madhav.sharma2002.12@gmail.com",
    url="https://github.com/Madhav89755/DjangoFast",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "django_fast": [
            "templates/project_template/*",
            "templates/project_template/**/*",
        ],
    },
    install_requires=[
        "django>=4.2,<5.0",
        "uvicorn>=0.22,<1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

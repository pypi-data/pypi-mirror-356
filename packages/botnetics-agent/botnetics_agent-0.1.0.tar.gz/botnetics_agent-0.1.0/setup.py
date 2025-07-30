from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="botnetics-agent",
    version="0.1.0",
    author="Behokus",
    author_email="behokus@proton.me",
    description="Simple framework for building Telegram agents with Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Behokus/botnetics-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0,<5.0",
        "django-cors-headers>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "botnetics=botnetics.cli:main",
        ],
    },
)

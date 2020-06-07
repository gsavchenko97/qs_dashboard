import setuptools
import qs_dashboard
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r", encoding="utf8") as f:
    required = f.read().splitlines()
print(os.path.join(
                "locales", "ru", "LC_MESSAGES", "*.mo"))
setuptools.setup(
    name="qs_dashboard",
    version=qs_dashboard.__version__,
    description="qs_dashboard is a tool for self checking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adis Davletov, Boris Sheludko",
    url="https://github.com/gsavchenko97/qs_dashboard",
    packages=setuptools.find_packages(),
    package_data={
        "qs_dashboard": [
            os.path.join(
                "locales", "ru", "LC_MESSAGES", "*.mo"),
            os.path.join(
                "locales", "ru", "LC_MESSAGES", "*.po")
        ],
    },
    entry_points={
        'console_scripts': [
            'qs_dashboard = qs_dashboard.cli:main',
        ],
    },
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

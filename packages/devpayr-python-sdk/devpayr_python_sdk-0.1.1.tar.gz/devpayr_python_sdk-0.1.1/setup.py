from setuptools import setup, find_packages

setup(
    name="devpayr-python-sdk",
    version="0.1.1",
    description="Framework-agnostic Python SDK for DevPayr – License enforcement, injectables, and project/license management",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="XulTech",
    author_email="support@devpayr.com",
    url="https://github.com/Xultech-LTD/devpayr_python_sdk",
    project_urls={
        "Homepage": "https://devpayr.com",
        "Documentation": "https://docs.devpayr.com",
        "Issues": "https://github.com/Xultech-LTD/devpayr_python_sdk/issues",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    install_requires=[
        "requests==2.32.4",
        "cryptography==44.0.1"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Build Tools"
    ],
    keywords=[
        "DevPayr", "SDK", "license", "license-key", "injectables",
        "project-management", "framework-agnostic", "encryption", "api-client"
    ],
)

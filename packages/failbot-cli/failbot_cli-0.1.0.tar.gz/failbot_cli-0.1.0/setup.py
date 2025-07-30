from setuptools import setup, find_packages

setup(
    name="failbot-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "typer[all]",
        "rich",
        "pyserial",
    ],
    entry_points={
        "console_scripts": [
            "failbot-cli=failbot.cli:app",
        ],
    },
    author="Failbot Team",
    author_email="team@failbot.com",
    description="CLI tool for uploading robot logs to Failbot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/failbot/failbot-cli",
    license="MIT",
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
) 
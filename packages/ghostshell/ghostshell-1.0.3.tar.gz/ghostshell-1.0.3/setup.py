
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ghostshell",
    version="1.0.3",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "ghostshell = ghostshell.cli.main:main"
        ]
    },
    author="Santhosh Murugesan",
    author_email="santhoshm.murugesan@gmail.com",
    description="Netcat-style remote command execution using Python socket.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Intended Audience :: Developers",
    "Topic :: Security",
    "Topic :: System :: Networking"
    ],
    python_requires='>=3.6',
    license="MIT"
    
)

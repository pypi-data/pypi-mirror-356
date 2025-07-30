from setuptools import setup, find_packages

setup(
    name="win32-scdump",
    version="0.1.0",
    author="AleirJDawn",
    author_email="",
    description="Scylla Process Dumper is a lightweight and easy-to-use debugging tool designed to create dumps of running processes on Windows using Scylla",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),   
    python_requires='>=3.6', 
    include_package_data=True,
    package_data={
        'win32_scdump': ['*.exe', '*.dll'],
    },
    entry_points={     
        'console_scripts': [
            'scdump=win32_scdump.main:main', 
        ],
    },
    classifiers=[      
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

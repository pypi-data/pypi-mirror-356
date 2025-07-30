from setuptools import setup, find_packages

setup(
    name="win32-show",
    version="0.1.0",
    author="AleirJDawn",
    author_email="",
    description="A script to find files and open them in Explorer",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),   
    python_requires='>=3.6', 
    entry_points={     
        'console_scripts': [
            'show=win32_show.main:main', 
        ],
    },
    classifiers=[      
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
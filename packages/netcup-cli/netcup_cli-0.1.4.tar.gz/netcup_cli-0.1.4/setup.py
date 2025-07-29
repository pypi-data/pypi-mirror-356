from setuptools import setup, find_packages

setup(
    name="netcup-cli", 
    version="0.1.4", 
    description="CLI tool for interacting with the Netcup Webservice",
    long_description=open('README.md').read(), 
    long_description_content_type="text/markdown", 
    author="Mihnea-Octavian Manolache", 
    author_email="me@mihnea.dev",  
    packages=find_packages(),  
    entry_points={
        'console_scripts': [
            'netcup-cli = netcup_cli.main:main',  
        ]
    },
    install_requires=[
        'zeep', 
        'netcup_webservice'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
)


from setuptools import setup, find_packages
import os 

# Function to read the requirements.txt file
def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()
    
# REQUIREMENTS = read_requirements()
REQUIREMENTS = ['azure-kusto-data==4.6.3', 'azure-eventhub','tenacity']
setup(
    name='fabricdataingest',
    version='0.1.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=REQUIREMENTS,
    # Additional metadata
    author='Angelica Garrido',
    author_email='agarrido@microsoft.com',
    description='Setup for Data Ingestion Framework',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
from setuptools import setup, find_packages

setup(
    name="vrep",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.2.1",
        "matplotlib>=3.8.2",
        "pyvis>=0.3.2",
        "pyyaml>=6.0.1",
        "scipy>=1.11.0"
    ],
    entry_points={
        'console_scripts': [
            'vrep=vrep.orchestrator:main',
        ],
    },
    author="Anonymous",
    description="A tool for visualizing repository dependencies",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/vrep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
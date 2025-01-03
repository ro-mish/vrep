from setuptools import setup, find_packages

setup(
    name="vrep",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.0",
        "matplotlib>=3.7.0",
        "pillow>=9.5.0",
        "graphviz>=0.20.1",
        "pyvis>=0.3.2",
        "pyyaml>=6.0.1",
        "scipy>=1.11.0",
        "gitpython>=3.1.0",
    ],
    extras_require={
        "all": [
            "networkx>=3.0",
            "matplotlib>=3.7.0",
            "pillow>=9.5.0",
            "graphviz>=0.20.1",
            "pyvis>=0.3.2",
            "pyyaml>=6.0.1",
            "scipy>=1.11.0",
            "gitpython>=3.1.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vrep=vrep.orchestrator:main",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for visualizing git repository commit history",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vrep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
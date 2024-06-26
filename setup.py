from setuptools import setup, find_packages

# Function to read requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read the requirements
requirements = parse_requirements('requirements.txt')

setup(
    name="securiti-automation",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "securiti-automation=program:main",
        ],
    },
)

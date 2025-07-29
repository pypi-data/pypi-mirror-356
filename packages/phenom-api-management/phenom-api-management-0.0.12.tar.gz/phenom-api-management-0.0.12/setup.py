from setuptools import setup, find_packages
VERSION = '0.0.12'
DESCRIPTION = 'Phenom Public Apis SDK for Python'
def read_readme():
    with open('README.md', 'r') as f:
        return f.read()
# Setting up
setup(
    name="phenom-api-management",
    version=VERSION,
    author="phenom",
    author_email="api-management@phenom.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=read_readme(),
    packages=find_packages(),
    install_requires=['PyJWT==2.4.0', 'certifi==2024.2.2', 'urllib3==1.26.18', 'six==1.16.0'],
    keywords=['resumeparser', 'exsearch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
    ]
)
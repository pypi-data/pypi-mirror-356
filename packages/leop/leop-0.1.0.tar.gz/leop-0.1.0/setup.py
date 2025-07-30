from setuptools import setup, find_packages

setup(
    name='leop',
    version='0.1.0',
    author='Leo',
    author_email='lindb2020@hotmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    license='MIT',
    license_file='LICENSE', 
    description='leop',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
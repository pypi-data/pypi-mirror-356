from setuptools import setup, find_packages

setup(
    name='mymath-shebin',  
    version='0.1.1',
    description='A simple math package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shebin',
    author_email='shebin212005@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)

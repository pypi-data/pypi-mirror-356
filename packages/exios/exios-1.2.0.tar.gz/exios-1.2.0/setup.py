from setuptools import setup, find_packages

setup(
    name='exios',
    version='1.2.0',
    author='Nitrix',
    author_email='nitrixexe@outlook.com',
    description='Async FastAPI-style wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nitrix4ly/exios',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)

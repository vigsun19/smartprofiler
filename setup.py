from setuptools import setup, find_packages

setup(
    name='SmartProfiler',
    version='0.3.0',
    packages=find_packages(),
    description='A lightweight, thread-safe Python library for profiling both execution time and memory usage.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vignesh Sundaram',
    author_email='vigneshanm@gmail.com',
    url='https://github.com/vigsun19/quick_profile',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

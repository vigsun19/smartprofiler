from setuptools import setup, find_packages

setup(
    name='smartprofiler',
    version='0.3.2',
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    description='A lightweight, thread-safe Python library and 1-stop shop for profiling execution time, memory usage, CPU time, and function call counts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vignesh Sundaram',
    author_email='vigneshanm@gmail.com',
    url='https://github.com/vigsun19/smartprofiler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

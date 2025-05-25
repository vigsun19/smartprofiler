from setuptools import setup, find_packages

# Safely read the README.md file for long_description
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A comprehensive Python library for profiling CPU, disk, memory, network I/O, and function calls with integrated visualization."

setup(
    name='smartprofiler',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.5.0',
        'numpy>=1.21.0',
        'requests>=2.28.0',
        'psutil>=5.9.0',  # Added for NetworkProfiler and DiskProfiler
    ],
    description='A comprehensive Python library for profiling CPU, disk, memory, network I/O, and function calls with integrated visualization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vignesh Sundaram',
    author_email='vigneshanm@gmail.com',
    url='https://github.com/vigsun19/smartprofiler',
    license='MIT',  # Added license field
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',  # Added Python 3.12 support
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    include_package_data=True,  # Ensure non-code files are included
)

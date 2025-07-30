from setuptools import setup, find_packages

setup(
    name='voltlogger',
    version='0.1.0',
    description='A lightweight logger for Python CLI tools and scripts',
    author='Voltur',
    url='https://github.com/stuarttempleton/volt-logger',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.7',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)

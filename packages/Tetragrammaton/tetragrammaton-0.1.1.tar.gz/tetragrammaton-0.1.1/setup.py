from setuptools import setup, find_packages

setup(
    name='Tetragrammaton',
    version='0.1.1',
    author='suiGn',
    description='Tetragrammaton library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
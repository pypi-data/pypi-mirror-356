from setuptools import setup, find_packages

setup(
    name='crosslang-wrapper-test',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='insanely_tamojit',
    description='Python SDK for Wrapper via REST API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
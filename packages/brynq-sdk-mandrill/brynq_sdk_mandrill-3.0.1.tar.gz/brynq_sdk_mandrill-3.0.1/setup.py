from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_mandrill',
    version='3.0.1',
    description='Mandrill wrapper from BrynQ',
    long_description='Mandrill wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    package_data={'brynq_sdk_mandrill': ['templates/*']},
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'mandrill-really-maintained>=1,<=2'
    ],
    zip_safe=False,
)
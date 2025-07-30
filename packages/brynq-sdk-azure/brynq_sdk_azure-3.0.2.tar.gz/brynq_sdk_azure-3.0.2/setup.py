from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_azure',
    version='3.0.2',
    description='Azure wrapper from BrynQ',
    long_description='Azure wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'azure-storage-file-share>=12.6.0',
        'azure-storage-blob>=12.16.0',
        'msal==1.22.0'
    ],
    zip_safe=False,
)

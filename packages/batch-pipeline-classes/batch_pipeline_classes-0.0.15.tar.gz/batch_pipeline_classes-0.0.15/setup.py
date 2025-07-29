from setuptools import setup, find_packages

setup(
    name='batch-pipeline-classes',
    version='0.0.15',
    packages=find_packages(),
    install_requires=[
        "google-cloud-bigquery",
        "boto3"
    ],
)

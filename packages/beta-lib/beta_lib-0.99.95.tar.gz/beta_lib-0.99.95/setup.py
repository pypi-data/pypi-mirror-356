from setuptools import setup, find_packages

setup(
    # name='Nyalytix-data-beacon',
    name="beta-lib",
    version='0.99.95',
    description="Nyalytix is a smart orchestration for data transformation engine that blends the essence of data and "
                "it's analytics to"
                "turn raw data into clean, insightful, and ML-ready pipelines.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='@KasturingAI',
    url='https://github.com/KasturingAI-ORG/pypi-libraries',
    license='Apache Software License 2.0',
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18",
        "pandas>=1.0",
        "plotly>=5.0"
    ],
    python_requires='>=3.7'

)

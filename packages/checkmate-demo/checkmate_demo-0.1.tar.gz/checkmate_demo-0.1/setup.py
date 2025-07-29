from setuptools import setup, find_packages

setup(
    name="checkmate-demo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "boto3",
        "python-dotenv",  # 'dotenv' should be 'python-dotenv' on PyPI
        "pyyaml",  # 'yaml' should be 'pyyaml' on PyPI
        "psycopg2",
        "redshift-connector",
        "sqlalchemy-redshift",
        "apscheduler",
        "croniter",
        "jinja2",
        "tabulate",
        "simpleeval",
        "spacy"
    ],
    entry_points={
        'console_scripts': [
            'dqtool = cli.dqtoolcli:main',
        ],
    },
)

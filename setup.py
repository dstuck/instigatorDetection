from setuptools import find_packages, setup

setup(
    name='instigator_detection',
    version='0.0.1',
    author='David Stück',
    author_email='david.e.stuck@gmail.com',
    packages=find_packages(),
    install_requires=[
        "python-twitter",
        "pyyaml",
        "SQLAlchemy>=1.3.0",
        "alembic==1.0.0",
        "psycopg2==2.7.5",
    ],
)

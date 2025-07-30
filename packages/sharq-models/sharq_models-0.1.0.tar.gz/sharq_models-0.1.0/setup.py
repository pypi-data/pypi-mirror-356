from setuptools import setup, find_packages

setup(
    name="sharq_models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "alembic==1.16.2",
        "asyncpg==0.30.0",
        "SQLAlchemy==2.0.41",
        "pydantic==2.11.7",
        "pydantic-settings==2.9.1",
        "python-dotenv==1.1.0",
    ],  
    author="Bekzod",
    author_email="pterest160@gmail.com",
    description="A package for Sharq project models",  # Update this with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

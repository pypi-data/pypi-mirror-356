# setup.py
from setuptools import setup, find_packages

setup(
    name="model_jacket",
    version="0.2.0",
    description="Package any ML model into a scalable, observable FastAPI service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shahwar Saleem",
    author_email="saleemshahwar@email.com",
    url="https://github.com/shahwarcodes/model-jacket",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "prometheus_client",
        "torch",
        "onnxruntime",
        "scikit-learn",
        "joblib"
    ],
    entry_points={
        "console_scripts": [
            "jacket=jacket_cli.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

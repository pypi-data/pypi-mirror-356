from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gchatbot",
    version="0.2.4",
    author="João Matheus & Guilherme Fialho",
    author_email="guilhermec.fialho@gmail.com",
    description="Biblioteca Python para criar bots para o Google Chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guilhermecf10/gchatbot",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-auth>=2.0.0",
        "google-api-python-client>=2.0.0",
        "google-apps-chat>=0.0.0",
        "protobuf>=3.19.0"
    ],
    extras_require={
        "fastapi": ["fastapi>=0.70.0", "uvicorn>=0.15.0"],
        "flask": ["flask>=2.0.0"],
    },
)

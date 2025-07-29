from setuptools import setup, find_packages

setup(
    name="toolwrap-lite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Gagan Naidu",
    description="Auto-generate OpenAI-compatible tool schemas from Python functions using decorators.",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
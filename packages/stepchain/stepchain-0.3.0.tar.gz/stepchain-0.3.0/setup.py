from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stepchain",
    version="0.3.0",
    author="TaskCrew Team",
    author_email="team@taskcrew.ai",
    description="The thinnest possible layer for reliable AI workflows - 185 lines, zero complexity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taskcrewai/stepchain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=[
        "pydantic>=2.0",
        "rich>=13.0",
        "pyyaml>=6.0",
        "opentelemetry-sdk>=1.20",
        "opentelemetry-exporter-otlp>=1.20",
        "openai>=1.0",
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "stepchain=stepchain.cli.main:main",
        ],
    },
)